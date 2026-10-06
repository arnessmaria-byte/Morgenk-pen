using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;

namespace BondeRavn.Coach
{
    /// <summary>
    /// Ravnens hjerne. Ren C#: tar en FarmReport og lager prioriterte råd og hendelser.
    /// Ingen Unity- eller Valheim-avhengigheter, så logikken kan testes utenfor spillet.
    /// </summary>
    public sealed class CoachBrain
    {
        private sealed class AnimalMemory
        {
            public bool Tamed;
            public bool Pregnant;
            public bool Seen;
            public int Level;
        }

        private readonly Dictionary<int, AnimalMemory> _memory = new Dictionary<int, AnimalMemory>();
        private readonly Dictionary<string, int> _bestStarsSeen = new Dictionary<string, int>();
        private readonly Dictionary<string, double> _lastSaid = new Dictionary<string, double>();
        private readonly Queue<Tip> _events = new Queue<Tip>();
        private readonly Random _rng;

        private List<Tip> _tips = new List<Tip>();
        private Tip _current;
        private double _currentSince = double.NegativeInfinity;
        private bool _firstReport = true;

        /// <summary>Hvor lenge ett råd står før neste velges.</summary>
        public double TipIntervalSec = 14;

        /// <summary>Hvor lenge ravnen venter før den gjentar samme råd.</summary>
        public double RepeatCooldownSec = 90;

        /// <summary>Slå av småprat når det ikke er noe å si.</summary>
        public bool Chatter = true;

        public CoachBrain(int seed = 0)
        {
            _rng = seed == 0 ? new Random() : new Random(seed);
        }

        public IReadOnlyList<Tip> CurrentTips => _tips;

        /// <summary>Sant når linjen som vises nå er en hendelse (noe som nettopp skjedde).</summary>
        public bool CurrentIsEvent => _current != null && _current.IsEvent;

        // ------------------------------------------------------------------
        // Analyse
        // ------------------------------------------------------------------

        public List<Tip> Analyze(FarmReport report)
        {
            var tips = new List<Tip>();
            DetectEvents(report);

            var animals = report.Animals.Where(a => a.Tameable || a.IsYoung).ToList();
            var tamed = animals.Where(a => a.Tamed && !a.IsYoung).ToList();
            var wild = animals.Where(a => !a.Tamed && a.Tameable && !a.IsYoung).ToList();
            var young = animals.Where(a => a.IsYoung).ToList();

            foreach (var group in tamed.GroupBy(a => a.Prefab))
            {
                AnalyzeHerd(group.Key, group.ToList(), young, tips);
            }

            AnalyzeWild(wild, tamed, tips);
            AnalyzeYoung(young, tips);
            AnalyzePlants(report.Plants, tips);

            if (tips.Count == 0 && Chatter)
            {
                tips.Add(new Tip("idle", 1, IdleLine(tamed.Count, wild.Count)));
            }

            _tips = tips.OrderByDescending(t => t.Priority).ToList();
            _firstReport = false;
            return _tips;
        }

        private void AnalyzeHerd(string prefab, List<AnimalInfo> herd, List<AnimalInfo> young, List<Tip> tips)
        {
            string species = herd[0].Species;
            int best = herd.Max(a => a.Level);
            int worst = herd.Min(a => a.Level);
            var foods = FoodList(herd);

            // 1. Sult stopper både temming og avl.
            var hungry = herd.Where(a => a.Hungry).ToList();
            if (hungry.Count > 0)
            {
                string who = hungry.Count == herd.Count
                    ? "Alle " + herd.Count + " " + species.ToLowerInvariant()
                    : hungry.Count + " av " + herd.Count + " " + species.ToLowerInvariant();
                tips.Add(new Tip("hungry:" + prefab, 95,
                    who + " er sultne. Sultne dyr får ikke unger. Kast " + foods + " inn i innhegningen; "
                    + "ett måltid metter i " + FormatTime(herd[0].FedDurationSec) + "."));
            }

            // 2. Urolige dyr (fiender i nærheten) parer seg ikke.
            var alerted = herd.Where(a => a.Alerted).ToList();
            if (alerted.Count > 0)
            {
                tips.Add(new Tip("alerted:" + prefab, 88,
                    alerted.Count + " " + species.ToLowerInvariant() + " er urolige. Avl stopper så lenge de er alarmert. "
                    + "Sjekk etter fiender rundt innhegningen (grådverger, skjeletter, ulv) og rydd opp."));
            }

            // 3. Stjernestrategi.
            if (best > worst)
            {
                tips.Add(new Tip("mixed:" + prefab, 82,
                    "Blandet stamme av " + species.ToLowerInvariant() + " (" + StarSpan(worst, best) + "). "
                    + "Ungen arver stjernene til den som blir gravid, og hvem som helst kan bli gravid. "
                    + "Sett " + StarAdj(best) + " for seg selv i egen innhegning, ellers blir mange av ungene dårlige."));
            }
            else if (best == 3)
            {
                tips.Add(new Tip("pure2:" + prefab, 30,
                    "Ren " + StarAdj(3) + " stamme av " + species.ToLowerInvariant() + ". Alle unger blir "
                    + Stars(3) + ". Hold dem mette og i fred, så ruller det på."));
            }
            else
            {
                tips.Add(new Tip("ceiling:" + prefab, 45,
                    "Alle " + species.ToLowerInvariant() + " her er " + Stars(best) + ". Avl kan aldri ØKE stjerner, bare arve dem. "
                    + "Vil du ha " + Stars(3) + " må du temme et vilt " + StarAdj(3) + " " + species.ToLowerInvariant()
                    + " (sjeldne, omtrent 1 av 100, oftere langt fra kartets midte)."));
            }

            // 4. Plass: for mange av samme art innenfor sjekkradius stopper avl.
            var crowded = herd.Where(a => a.CanProcreate && a.MaxCreatures > 0 && a.SameKindWithinTotalRange >= a.MaxCreatures).ToList();
            if (crowded.Count > 0)
            {
                var sample = crowded[0];
                string cull = best > worst
                    ? " Slakt eller flytt de med færrest stjerner (" + Stars(worst) + ")."
                    : " Slakt noen, eller lag en innhegning til lenger unna.";
                tips.Add(new Tip("crowded:" + prefab, 80,
                    "Fullt hus: " + sample.SameKindWithinTotalRange + " " + species.ToLowerInvariant() + " innenfor "
                    + Meters(sample.TotalCheckRange) + " (grensen er " + sample.MaxCreatures + "). Ingen nye unger før det er færre." + cull));
            }

            // 5. Gravide.
            foreach (var a in herd.Where(a => a.Pregnant).OrderBy(a => a.DueInSec))
            {
                int offspringLevel = Math.Max(a.MinOffspringLevel, a.Level);
                tips.Add(new Tip("pregnant:" + a.Id, 60,
                    Name(a) + " er gravid og føder om " + FormatTime(a.DueInSec) + ". Ungen blir " + Stars(offspringLevel) + "."));
            }

            // 6. Ensomme.
            var lonely = herd.Where(a => a.CanProcreate && !a.Pregnant && !a.Hungry && a.PartnersWithinPartnerRange == 0).ToList();
            if (lonely.Count > 0 && herd.Count >= 2)
            {
                var a = lonely[0];
                tips.Add(new Tip("lonely:" + prefab, 70,
                    Name(a) + " står for langt fra de andre. Minst to tamme " + species.ToLowerInvariant()
                    + " må stå innenfor " + Meters(a.PartnerCheckRange) + " av hverandre for å pare seg. Lokk dem sammen med mat."));
            }
            else if (herd.Count == 1 && herd[0].CanProcreate)
            {
                var a = herd[0];
                tips.Add(new Tip("single:" + prefab, 65,
                    Name(a) + " er alene. Du trenger minst to tamme " + species.ToLowerInvariant() + " for avl. "
                    + "Tam en til, helst med like mange stjerner (" + Stars(a.Level) + ")."));
            }

            // 7. Kjærlighetspoeng (fremdrift mot graviditet).
            var courting = herd.Where(a => a.CanProcreate && !a.Pregnant && !a.Hungry && a.PartnersWithinPartnerRange > 0)
                .OrderByDescending(a => a.LovePoints).ToList();
            if (courting.Count > 0)
            {
                var a = courting[0];
                string chance = ((int)Math.Round(a.PregnancyChance * 100)).ToString(CultureInfo.InvariantCulture);
                tips.Add(new Tip("love:" + prefab, 40,
                    Name(a) + " koser seg med partner: kjærlighet " + a.LovePoints + "/" + a.RequiredLovePoints + ". "
                    + "Spillet triller terning hvert " + FormatTime(a.ProcreationIntervalSec) + " med " + chance + " % sjanse for et poeng."));
            }
        }

        private void AnalyzeWild(List<AnimalInfo> wild, List<AnimalInfo> tamed, List<Tip> tips)
        {
            foreach (var a in wild.OrderByDescending(a => a.Level).ThenBy(a => a.DistanceToPlayer))
            {
                bool inProgress = a.TamingTotalSec > 0 && a.TamingLeftSec < a.TamingTotalSec - 1f;
                int bestTamed = tamed.Where(t => t.Prefab == a.Prefab).Select(t => t.Level).DefaultIfEmpty(0).Max();
                string foods = FoodList(new List<AnimalInfo> { a });

                if (inProgress)
                {
                    float pct = 100f * (1f - a.TamingLeftSec / Math.Max(1f, a.TamingTotalSec));
                    string state;
                    if (a.Alerted)
                        state = " Den er redd nå: gå ut av syne, temming teller bare når den er rolig.";
                    else if (a.Hungry)
                        state = " Den er sulten: kast mer " + foods + " så klokka går.";
                    else
                        state = " Rolig og mett, klokka går. Hold avstand.";
                    tips.Add(new Tip("taming:" + a.Id, 86,
                        "Temming av " + StarAdj(a.Level) + " " + a.Species.ToLowerInvariant() + ": " + pct.ToString("0", CultureInfo.InvariantCulture)
                        + " %, " + FormatTime(a.TamingLeftSec) + " igjen." + state));
                }
                else
                {
                    int prio = a.Level > bestTamed ? 75 : 35;
                    string pitch = a.Level > bestTamed && bestTamed > 0
                        ? " Bedre enn det du har i fjøset! "
                        : a.Level == 3 ? " Jackpot! " : " ";
                    tips.Add(new Tip("wild:" + a.Id, prio,
                        "Vilt " + StarAdj(a.Level) + " " + a.Species.ToLowerInvariant() + " " + Meters(a.DistanceToPlayer) + " unna." + pitch
                        + "Gjerd det inne, kast " + foods + ", og gå unna så det roer seg. Full temming tar " + FormatTime(a.TamingTotalSec) + " rolig tid."));
                }
            }
        }

        private void AnalyzeYoung(List<AnimalInfo> young, List<Tip> tips)
        {
            if (young.Count == 0) return;
            var next = young.OrderBy(a => a.GrowUpInSec).First();
            tips.Add(new Tip("young", 32,
                young.Count + (young.Count == 1 ? " unge vokser opp. Den" : " unger vokser opp. Den første")
                + " blir voksen om " + FormatTime(next.GrowUpInSec) + ". Unger teller med i plassgrensen, så ikke la innhegningen bli full."));
        }

        private void AnalyzePlants(List<PlantInfo> plants, List<Tip> tips)
        {
            if (plants == null || plants.Count == 0) return;

            int noSpace = plants.Count(p => p.Status == "NoSpace");
            int wrongBiome = plants.Count(p => p.Status == "WrongBiome");
            int notCultivated = plants.Count(p => p.Status == "NotCultivated");
            int noSun = plants.Count(p => p.Status == "NoSun");
            int tooCold = plants.Count(p => p.Status == "TooCold" || p.Status == "TooHot");
            int ready = plants.Count(p => !float.IsNaN(p.ReadyInSec) && p.ReadyInSec <= 0f);

            if (noSpace > 0)
                tips.Add(new Tip("plant:space", 50, noSpace + " planter står for tett og vil visne. Flytt dem; gi hver plante omtrent to meter."));
            if (wrongBiome > 0)
                tips.Add(new Tip("plant:biome", 50, wrongBiome + " planter står i feil biom og vokser ikke. Sjekk hvor arten hører hjemme."));
            if (notCultivated > 0)
                tips.Add(new Tip("plant:soil", 48, notCultivated + " planter står på udyrket jord. Bruk kultivatoren først."));
            if (noSun > 0)
                tips.Add(new Tip("plant:sun", 44, noSun + " planter mangler lys. Fjern tak eller flytt dem ut."));
            if (tooCold > 0)
                tips.Add(new Tip("plant:temp", 44, tooCold + " planter har feil temperatur og vokser ikke her."));
            if (ready > 0)
                tips.Add(new Tip("plant:ready", 38, ready + " planter er klare til høsting. Ferdig mat til grisene, Krra!"));
        }

        // ------------------------------------------------------------------
        // Hendelser (sammenligner med forrige rapport)
        // ------------------------------------------------------------------

        private void DetectEvents(FarmReport report)
        {
            var seenNow = new HashSet<int>();
            foreach (var a in report.Animals)
            {
                if (!a.Tameable && !a.IsYoung) continue;
                seenNow.Add(a.Id);

                AnimalMemory mem;
                bool known = _memory.TryGetValue(a.Id, out mem);
                if (!known)
                {
                    mem = new AnimalMemory();
                    _memory[a.Id] = mem;
                }

                if (known)
                {
                    if (!mem.Tamed && a.Tamed && !a.IsYoung)
                        _events.Enqueue(new Tip("ev:tamed:" + a.Id, 100,
                            "Krra! " + Name(a) + " er tam nå. " + Stars(a.Level) + " i fjøset!", true));

                    if (!mem.Pregnant && a.Pregnant)
                        _events.Enqueue(new Tip("ev:preg:" + a.Id, 100,
                            Name(a) + " er gravid! Ungen kommer om " + FormatTime(a.DueInSec) + " og blir "
                            + Stars(Math.Max(a.MinOffspringLevel, a.Level)) + ".", true));
                }
                else if (!_firstReport && a.IsYoung && a.Tamed && a.DistanceToPlayer < 40f)
                {
                    _events.Enqueue(new Tip("ev:born:" + a.Id, 100,
                        "En ny unge! " + a.Species + ", " + Stars(a.Level) + ".", true));
                }

                int bestSeen;
                _bestStarsSeen.TryGetValue(a.Prefab, out bestSeen);
                if (!a.Tamed && a.Tameable && a.Level > bestSeen && a.Level >= 2 && !_firstReport)
                {
                    _events.Enqueue(new Tip("ev:star:" + a.Id, 100,
                        "Oi! Et vilt " + StarAdj(a.Level) + " " + a.Species.ToLowerInvariant() + " " + Meters(a.DistanceToPlayer) + " unna. Ikke drep det, tam det!", true));
                }
                if (a.Level > bestSeen) _bestStarsSeen[a.Prefab] = a.Level;

                mem.Tamed = a.Tamed;
                mem.Pregnant = a.Pregnant;
                mem.Level = a.Level;
                mem.Seen = true;
            }

            // Glem dyr som ikke lenger er lastet, så minnet ikke vokser evig.
            var gone = _memory.Keys.Where(id => !seenNow.Contains(id)).ToList();
            foreach (var id in gone) _memory.Remove(id);
        }

        // ------------------------------------------------------------------
        // Hva ravnen sier akkurat nå
        // ------------------------------------------------------------------

        /// <summary>Returnerer linjen ravnen skal vise nå, eller null hvis den tier.</summary>
        public string Speak(double now)
        {
            if (_events.Count > 0 && (_current == null || !_current.IsEvent || now - _currentSince >= TipIntervalSec * 0.6))
            {
                SetCurrent(_events.Dequeue(), now);
                return Render(_current);
            }

            if (_current == null || now - _currentSince >= TipIntervalSec)
            {
                var next = PickNext(now);
                if (next != null) SetCurrent(next, now);
                else _current = null;
            }

            return _current == null ? null : Render(_current);
        }

        /// <summary>Tvinger ravnen til å si en bestemt ting nå (brukes ved hurtigtaster o.l.).</summary>
        public void Say(string text, double now)
        {
            SetCurrent(new Tip("say", 100, text, true), now);
        }

        private Tip PickNext(double now)
        {
            if (_tips.Count == 0) return null;

            foreach (var tip in _tips)
            {
                double last;
                bool said = _lastSaid.TryGetValue(tip.Key, out last);
                double cooldown = tip.Priority >= 85 ? RepeatCooldownSec * 0.4 : RepeatCooldownSec;
                if (!said || now - last >= cooldown) return tip;
            }

            // Alt er nylig sagt: ti stille til nedkjølingen er over (hastesaker har kortere nedkjøling).
            return null;
        }

        private void SetCurrent(Tip tip, double now)
        {
            _current = tip;
            _currentSince = now;
            _lastSaid[tip.Key] = now;
        }

        private string Render(Tip tip)
        {
            return tip.Text;
        }

        // ------------------------------------------------------------------
        // Oversiktstavle
        // ------------------------------------------------------------------

        public string BuildBoard(FarmReport report)
        {
            var sb = new StringBuilder();
            var animals = report.Animals.Where(a => a.Tameable || a.IsYoung).ToList();
            if (animals.Count == 0)
            {
                sb.Append("Ingen dyr i nærheten.");
                return sb.ToString();
            }

            foreach (var group in animals.GroupBy(a => a.Prefab).OrderByDescending(g => g.Count(x => x.Tamed)))
            {
                var list = group.ToList();
                var tamed = list.Where(a => a.Tamed).ToList();
                var wild = list.Where(a => !a.Tamed).ToList();
                string species = list[0].Species;

                sb.Append(species).Append(": ");
                if (tamed.Count > 0)
                {
                    sb.Append(tamed.Count).Append(" tamme [");
                    sb.Append(string.Join(", ", new[] { 1, 2, 3 }
                        .Select(l => new { l, n = tamed.Count(a => a.Level == l) })
                        .Where(x => x.n > 0)
                        .Select(x => x.n + "x" + Stars(x.l))));
                    sb.Append("]");
                    int hungry = tamed.Count(a => a.Hungry);
                    int preg = tamed.Count(a => a.Pregnant);
                    int young = tamed.Count(a => a.IsYoung);
                    if (hungry > 0) sb.Append(", ").Append(hungry).Append(" sultne");
                    if (preg > 0) sb.Append(", ").Append(preg).Append(" gravide");
                    if (young > 0) sb.Append(", ").Append(young).Append(" unger");
                    var love = tamed.Where(a => a.CanProcreate && !a.Pregnant).OrderByDescending(a => a.LovePoints).FirstOrDefault();
                    if (love != null && love.RequiredLovePoints > 0)
                        sb.Append(", kjærlighet ").Append(love.LovePoints).Append('/').Append(love.RequiredLovePoints);
                }
                if (wild.Count > 0)
                {
                    if (tamed.Count > 0) sb.Append("; ");
                    sb.Append(wild.Count).Append(" ville (beste ").Append(Stars(wild.Max(a => a.Level))).Append(")");
                }
                sb.AppendLine();
            }

            if (report.Plants.Count > 0)
            {
                int ready = report.Plants.Count(p => !float.IsNaN(p.ReadyInSec) && p.ReadyInSec <= 0f);
                int bad = report.Plants.Count(p => p.Status != "Healthy");
                sb.Append("Planter: ").Append(report.Plants.Count);
                if (ready > 0) sb.Append(", ").Append(ready).Append(" klare");
                if (bad > 0) sb.Append(", ").Append(bad).Append(" mistrives");
                sb.AppendLine();
            }

            return sb.ToString().TrimEnd();
        }

        // ------------------------------------------------------------------
        // Småprat og formatering
        // ------------------------------------------------------------------

        private static readonly string[] IdleLines =
        {
            "Krra. Alt stille på gården. Jeg sier fra når noe skjer.",
            "Ingen dyr å se. Villsvin finner du på engene, gjerne nær bær og sopp.",
            "Husk: to stjerner på moren gir to stjerner på ungen. Alltid.",
            "En ravn ser alt. En bonde ser etter en ravn.",
            "Tips: en innhegning med fire-fem dyr innenfor ti meter er full. Bygg flere små.",
            "Odin sendte meg for å passe på grisene dine. Ikke spør.",
        };

        private string IdleLine(int tamedCount, int wildCount)
        {
            if (tamedCount == 0 && wildCount == 0)
                return IdleLines[_rng.Next(IdleLines.Length)];
            return IdleLines[0];
        }

        private static string Name(AnimalInfo a)
        {
            return string.IsNullOrEmpty(a.PetName)
                ? a.Species + " (" + Stars(a.Level) + ")"
                : a.PetName + " (" + a.Species.ToLowerInvariant() + ", " + Stars(a.Level) + ")";
        }

        private static string FoodList(List<AnimalInfo> herd)
        {
            var foods = herd.SelectMany(a => a.Foods).Where(f => !string.IsNullOrEmpty(f)).Distinct().Take(5).ToList();
            if (foods.Count == 0) return "mat de liker";
            if (foods.Count == 1) return foods[0].ToLowerInvariant();
            return string.Join(", ", foods.Take(foods.Count - 1).Select(f => f.ToLowerInvariant())) + " eller " + foods[foods.Count - 1].ToLowerInvariant();
        }

        public static string Stars(int level)
        {
            int stars = Math.Max(0, level - 1);
            if (stars == 0) return "0 stjerner";
            if (stars == 1) return "1 stjerne";
            return stars + " stjerner";
        }

        /// <summary>Adjektivform: "2-stjerners", til bruk foran et substantiv.</summary>
        public static string StarAdj(int level)
        {
            return Math.Max(0, level - 1) + "-stjerners";
        }

        private static string StarSpan(int worstLevel, int bestLevel)
        {
            return Stars(worstLevel) + " til " + Stars(bestLevel);
        }

        public static string Meters(float m)
        {
            return ((int)Math.Round(m)).ToString(CultureInfo.InvariantCulture) + " m";
        }

        public static string FormatTime(float seconds)
        {
            if (float.IsNaN(seconds) || float.IsInfinity(seconds)) return "ukjent tid";
            if (seconds <= 0f) return "0 s";
            int s = (int)Math.Round(seconds);
            if (s < 60) return s + " s";
            int m = s / 60;
            int rest = s % 60;
            if (m < 60)
                return rest == 0 || m >= 10 ? m + " min" : m + " min " + rest + " s";
            int h = m / 60;
            int mm = m % 60;
            return mm == 0 ? h + " t" : h + " t " + mm + " min";
        }
    }
}
