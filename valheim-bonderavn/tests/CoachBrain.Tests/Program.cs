using System;
using System.Collections.Generic;
using System.Linq;
using BondeRavn.Coach;

namespace BondeRavn.Tests
{
    /// <summary>
    /// Enkle scenariotester for ravnens hjerne. Feiler med exit-kode 1 hvis en forventning ryker.
    /// </summary>
    internal static class Program
    {
        private static int _failures;

        private static int Main()
        {
            ScenarioMixedHerd();
            ScenarioHungryAndCrowded();
            ScenarioTamingInProgress();
            ScenarioEvents();
            ScenarioRotationAndCooldown();
            ScenarioFormatting();

            Console.WriteLine();
            Console.WriteLine(_failures == 0 ? "Alle scenarier OK." : _failures + " feil.");
            return _failures == 0 ? 0 : 1;
        }

        // ------------------------------------------------------------------

        private static AnimalInfo Boar(int id, int level, bool tamed = true, float x = 0, float z = 0)
        {
            return new AnimalInfo
            {
                Id = id, Prefab = "Boar", Species = "Villsvin", Level = level, Tamed = tamed,
                Tameable = true, TamingTotalSec = 1800, TamingLeftSec = tamed ? 0 : 1800, FedDurationSec = 600,
                Foods = new List<string> { "Gulrot", "Blåbær", "Bringebær", "Sopp" },
                CanProcreate = true, RequiredLovePoints = 4, MaxCreatures = 4, TotalCheckRange = 10,
                PartnerCheckRange = 3, PregnancyChance = 0.33f, PregnancyDurationSec = 60, ProcreationIntervalSec = 30,
                X = x, Z = z, DistanceToPlayer = (float)Math.Sqrt(x * x + z * z),
                SameKindWithinTotalRange = 1, PartnersWithinPartnerRange = 0,
            };
        }

        private static void Expect(bool cond, string what)
        {
            Console.WriteLine((cond ? "  ok   " : "  FEIL ") + what);
            if (!cond) _failures++;
        }

        private static void Dump(string title, IEnumerable<Tip> tips)
        {
            Console.WriteLine();
            Console.WriteLine("== " + title);
            foreach (var t in tips) Console.WriteLine("  " + t);
        }

        // ------------------------------------------------------------------

        private static void ScenarioMixedHerd()
        {
            var brain = new CoachBrain(1);
            var r = new FarmReport();
            var a = Boar(1, 3); var b = Boar(2, 1, x: 2); var c = Boar(3, 2, x: 1, z: 1);
            foreach (var x in new[] { a, b, c }) { x.SameKindWithinTotalRange = 3; x.PartnersWithinPartnerRange = 2; x.LovePoints = 2; }
            r.Animals.AddRange(new[] { a, b, c });

            var tips = brain.Analyze(r);
            Dump("Blandet stamme (0, 1 og 2 stjerner)", tips);
            Expect(tips.Any(t => t.Key == "mixed:Boar"), "råder til å skille ut 2-stjerners");
            Expect(tips.First().Key == "mixed:Boar", "stjernestrategi er viktigst når ingen er sultne");
            Expect(tips.Any(t => t.Key == "love:Boar" && t.Text.Contains("2/4")), "viser kjærlighetspoeng 2/4");
            Expect(!tips.Any(t => t.Key.StartsWith("lonely")), "ingen ensomme når partnere finnes");
        }

        private static void ScenarioHungryAndCrowded()
        {
            var brain = new CoachBrain(1);
            var r = new FarmReport();
            var herd = Enumerable.Range(1, 5).Select(i => Boar(i, 3, x: i * 0.5f)).ToList();
            foreach (var x in herd) { x.SameKindWithinTotalRange = 5; x.PartnersWithinPartnerRange = 4; }
            herd[0].Hungry = true; herd[1].Hungry = true;
            herd[2].Pregnant = true; herd[2].DueInSec = 42;
            r.Animals.AddRange(herd);

            var tips = brain.Analyze(r);
            Dump("Sultne og fullt hus", tips);
            Expect(tips.First().Key == "hungry:Boar", "sult kommer først");
            Expect(tips.First().Text.Contains("gulrot"), "matliste nevner gulrot");
            Expect(tips.Any(t => t.Key == "crowded:Boar" && t.Text.Contains("5 villsvin")), "fullt hus med 5 dyr");
            Expect(tips.Any(t => t.Key == "pregnant:3" && t.Text.Contains("42 s") && t.Text.Contains("2 stjerner")), "gravid med nedtelling og arvet stjerne");
            Expect(tips.Any(t => t.Key == "pure2:Boar"), "ren 2-stjerners stamme");

            Console.WriteLine(brain.BuildBoard(r));
            Expect(brain.BuildBoard(r).Contains("5 tamme [5x2 stjerner], 2 sultne, 1 gravide"), "tavla oppsummerer riktig");
        }

        private static void ScenarioTamingInProgress()
        {
            var brain = new CoachBrain(1);
            var r = new FarmReport();
            var tamed = Boar(1, 1);
            var wild = Boar(2, 3, tamed: false, x: 6);
            wild.TamingLeftSec = 900; wild.Alerted = true;
            var wild2 = Boar(3, 1, tamed: false, x: 20);
            r.Animals.AddRange(new[] { tamed, wild, wild2 });

            var tips = brain.Analyze(r);
            Dump("Temming pågår", tips);
            Expect(tips.First().Key == "taming:2" && tips.First().Text.Contains("50 %"), "temming 50 % øverst");
            Expect(tips.First().Text.Contains("redd"), "sier at dyret er redd");
            Expect(tips.Any(t => t.Key == "wild:3" && t.Priority == 35), "0-stjerners vilt er lavt prioritert når du har like bra");
            Expect(tips.Any(t => t.Key == "single:Boar"), "ett tamt dyr er alene");
        }

        private static void ScenarioEvents()
        {
            var brain = new CoachBrain(1);
            var r1 = new FarmReport();
            var wild = Boar(1, 3, tamed: false, x: 5);
            r1.Animals.Add(wild);
            brain.Analyze(r1);
            string first = brain.Speak(0);
            Console.WriteLine();
            Console.WriteLine("== Hendelser");
            Console.WriteLine("  t=0:  " + first);

            var r2 = new FarmReport();
            var nowTamed = Boar(1, 3, tamed: true, x: 5);
            r2.Animals.Add(nowTamed);
            brain.Analyze(r2);
            string second = brain.Speak(1);
            Console.WriteLine("  t=1:  " + second);
            Expect(second.Contains("er tam nå"), "hendelse når dyret blir tamt");
            Expect(brain.CurrentIsEvent, "hendelsen er merket som hendelse");

            var r3 = new FarmReport();
            var preg = Boar(1, 3, tamed: true, x: 5); preg.Pregnant = true; preg.DueInSec = 60;
            var baby = new AnimalInfo { Id = 9, Prefab = "Boar_piggy", Species = "Grisunge", Level = 3, Tamed = true, IsYoung = true, GrowUpInSec = 2500, DistanceToPlayer = 3 };
            r3.Animals.AddRange(new[] { preg, baby });
            brain.Analyze(r3);
            string third = brain.Speak(2);
            string fourth = brain.Speak(20);
            string fifth = brain.Speak(40);
            Console.WriteLine("  t=2:  " + third);
            Console.WriteLine("  t=20: " + fourth);
            Console.WriteLine("  t=40: " + fifth);
            Expect(fourth.Contains("gravid"), "hendelse når dyret blir gravid");
            Expect(fifth.Contains("ny unge"), "hendelse når en unge dukker opp");
        }

        private static void ScenarioRotationAndCooldown()
        {
            var brain = new CoachBrain(1) { TipIntervalSec = 10, RepeatCooldownSec = 100 };
            var r = new FarmReport();
            var a = Boar(1, 3); var b = Boar(2, 1, x: 2);
            foreach (var x in new[] { a, b }) { x.SameKindWithinTotalRange = 2; x.PartnersWithinPartnerRange = 1; }
            r.Animals.AddRange(new[] { a, b });
            brain.Analyze(r);

            var seen = new List<string>();
            for (double t = 0; t < 60; t += 10) seen.Add(brain.Speak(t));
            Console.WriteLine();
            Console.WriteLine("== Rotasjon");
            foreach (var s in seen) Console.WriteLine("  " + s);
            Expect(seen.Where(s => s != null).Distinct().Count() >= 2, "ravnen roterer mellom råd");
            Expect(seen[1] != seen[0], "nytt råd etter intervallet");
            Expect(seen.Skip(2).All(s => s == null), "tier når alt er sagt og nedkjølingen ikke er over");
            Expect(brain.Speak(130) != null, "snakker igjen etter nedkjølingen");
            string idle = new CoachBrain(1).Speak(0);
            Expect(idle == null, "tier før første rapport");
            var empty = new CoachBrain(1);
            empty.Analyze(new FarmReport());
            Expect(!string.IsNullOrEmpty(empty.Speak(0)), "småprater når gården er tom");
        }

        private static void ScenarioFormatting()
        {
            Console.WriteLine();
            Console.WriteLine("== Formatering");
            Expect(CoachBrain.FormatTime(45) == "45 s", "45 s");
            Expect(CoachBrain.FormatTime(90) == "1 min 30 s", "1 min 30 s");
            Expect(CoachBrain.FormatTime(1800) == "30 min", "30 min");
            Expect(CoachBrain.FormatTime(5400) == "1 t 30 min", "1 t 30 min");
            Expect(CoachBrain.Stars(1) == "0 stjerner" && CoachBrain.Stars(2) == "1 stjerne" && CoachBrain.Stars(3) == "2 stjerner", "stjernetekst");
        }
    }
}
