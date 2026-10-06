using System.Collections.Generic;

namespace BondeRavn.Coach
{
    /// <summary>
    /// Et øyeblikksbilde av gården, uten noen Unity- eller Valheim-typer.
    /// FarmScanner (spillsiden) fyller denne; CoachBrain (ren C#) leser den.
    /// </summary>
    public sealed class FarmReport
    {
        /// <summary>Spilltid i sekunder (monotont økende) da rapporten ble tatt.</summary>
        public double NowSeconds;

        public List<AnimalInfo> Animals = new List<AnimalInfo>();
        public List<PlantInfo> Plants = new List<PlantInfo>();
    }

    public sealed class AnimalInfo
    {
        /// <summary>Stabil id for dyret så lenge det er lastet (instans-id).</summary>
        public int Id;

        /// <summary>Prefab-navn, f.eks. "Boar", "Wolf", "Lox", "Boar_piggy".</summary>
        public string Prefab = "";

        /// <summary>Lokalisert artsnavn, f.eks. "Villsvin".</summary>
        public string Species = "";

        /// <summary>Kjælenavn gitt av spilleren, ellers tom.</summary>
        public string PetName = "";

        /// <summary>Spillets nivå: 1 = ingen stjerner, 2 = en stjerne, 3 = to stjerner.</summary>
        public int Level = 1;

        public bool Tamed;
        public bool Hungry;
        public bool Alerted;
        public float DistanceToPlayer;

        public float X, Y, Z;

        // Temming (Tameable)
        public bool Tameable;
        public float TamingTotalSec;
        public float TamingLeftSec;
        public float FedDurationSec;
        public List<string> Foods = new List<string>();

        // Avl (Procreation)
        public bool CanProcreate;
        public bool Pregnant;
        public float DueInSec;
        public int LovePoints;
        public int RequiredLovePoints;
        public int MaxCreatures;
        public float TotalCheckRange;
        public float PartnerCheckRange;
        public float PregnancyChance;
        public float PregnancyDurationSec;
        public float ProcreationIntervalSec;
        public int MinOffspringLevel;

        /// <summary>Antall dyr av samme art (tamme og ville) innenfor TotalCheckRange, inkludert dette.</summary>
        public int SameKindWithinTotalRange;

        /// <summary>Antall ANDRE tamme, ikke gravide dyr av samme art innenfor PartnerCheckRange.</summary>
        public int PartnersWithinPartnerRange;

        // Unge (Growup)
        public bool IsYoung;
        public float GrowUpInSec;

        public int Stars => Level - 1;

        public string DisplayName => string.IsNullOrEmpty(PetName) ? Species : PetName;
    }

    public sealed class PlantInfo
    {
        public string Name = "";
        /// <summary>Statusnavn fra spillet: Healthy, NoSun, NoSpace, WrongBiome, NotCultivated, TooCold, TooHot.</summary>
        public string Status = "Healthy";
        /// <summary>Sekunder til planten er ferdig vokst; negativ eller 0 betyr klar. NaN betyr ukjent.</summary>
        public float ReadyInSec = float.NaN;
    }
}
