namespace BondeRavn.Coach
{
    public sealed class Tip
    {
        /// <summary>Nøkkel for å unngå å gjenta samme råd for ofte, f.eks. "hungry:Boar".</summary>
        public string Key;

        /// <summary>Høyere tall vises først.</summary>
        public int Priority;

        public string Text;

        /// <summary>Hendelser (noe skjedde akkurat nå) vises straks og bare én gang.</summary>
        public bool IsEvent;

        public Tip(string key, int priority, string text, bool isEvent = false)
        {
            Key = key;
            Priority = priority;
            Text = text;
            IsEvent = isEvent;
        }

        public override string ToString() => "[" + Priority + "] " + Text;
    }
}
