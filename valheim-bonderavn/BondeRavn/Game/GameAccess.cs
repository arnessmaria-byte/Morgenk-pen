using System;
using System.Reflection;
using UnityEngine;

namespace BondeRavn.Game
{
    /// <summary>
    /// Små, versjonstolerante hjelpere mot spillets interne data.
    /// Alt som ikke er garantert offentlig i assembly_valheim hentes via refleksjon,
    /// og mangler noe faller vi stille tilbake til "ukjent".
    /// </summary>
    internal static class GameAccess
    {
        /// <summary>ZDO-nøkler slik spillet selv bruker dem (ZDOVars). Strengene hashes av ZDO.</summary>
        internal static class Keys
        {
            public const string TameTimeLeft = "TameTimeLeft";
            public const string TameLastFeeding = "TameLastFeeding";
            public const string TamedName = "TamedName";
            public const string LovePoints = "lovePoints";
            public const string Pregnant = "pregnant";
            public const string SpawnTime = "spawntime";
        }

        private static readonly MethodInfo PlantTimeSincePlanted =
            typeof(Plant).GetMethod("TimeSincePlanted", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);

        private static readonly MethodInfo PlantGetGrowTime =
            typeof(Plant).GetMethod("GetGrowTime", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);

        private static readonly FieldInfo PlantStatus =
            typeof(Plant).GetField("m_status", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);

        private static readonly FieldInfo PlantName =
            typeof(Plant).GetField("m_name", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);

        public static string PrefabName(GameObject go)
        {
            if (go == null) return "";
            string n = go.name;
            int i = n.IndexOf("(Clone)", StringComparison.Ordinal);
            return i >= 0 ? n.Substring(0, i) : n;
        }

        public static string Localize(string token)
        {
            if (string.IsNullOrEmpty(token)) return "";
            try
            {
                var loc = Localization.instance;
                if (loc != null) return loc.Localize(token);
            }
            catch (Exception)
            {
                // Faller tilbake til rå token under.
            }
            return token.TrimStart('$');
        }

        public static DateTime GameTime()
        {
            try
            {
                var net = ZNet.instance;
                if (net != null) return net.GetTime();
            }
            catch (Exception)
            {
            }
            return DateTime.Now;
        }

        public static ZDO ZdoOf(Component c)
        {
            if (c == null) return null;
            var nview = c.GetComponent<ZNetView>();
            if (nview == null) return null;
            try
            {
                return nview.IsValid() ? nview.GetZDO() : null;
            }
            catch (Exception)
            {
                return null;
            }
        }

        public static string PlantStatusName(Plant plant)
        {
            if (plant == null || PlantStatus == null) return "Healthy";
            try
            {
                var v = PlantStatus.GetValue(plant);
                return v == null ? "Healthy" : v.ToString();
            }
            catch (Exception)
            {
                return "Healthy";
            }
        }

        public static string PlantDisplayName(Plant plant)
        {
            if (plant == null || PlantName == null) return "";
            try
            {
                return Localize(PlantName.GetValue(plant) as string);
            }
            catch (Exception)
            {
                return "";
            }
        }

        /// <summary>Sekunder til planten er ferdig. NaN hvis spillversjonen ikke lar oss lese det.</summary>
        public static float PlantReadyInSeconds(Plant plant)
        {
            if (plant == null || PlantTimeSincePlanted == null || PlantGetGrowTime == null) return float.NaN;
            try
            {
                double since = Convert.ToDouble(PlantTimeSincePlanted.Invoke(plant, null));
                double grow = Convert.ToDouble(PlantGetGrowTime.Invoke(plant, null));
                return (float)(grow - since);
            }
            catch (Exception)
            {
                return float.NaN;
            }
        }

        /// <summary>Viser en melding i spillets eget HUD. Isolert i egen metode så en signaturendring bare rammer dette kallet.</summary>
        public static bool TryShowHudMessage(string text, bool center)
        {
            try
            {
                ShowHudMessageInner(text, center);
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        private static void ShowHudMessageInner(string text, bool center)
        {
            var hud = MessageHud.instance;
            if (hud == null) return;
            hud.ShowMessage(center ? MessageHud.MessageType.Center : MessageHud.MessageType.TopLeft, text);
        }

        public static bool HudHidden()
        {
            try
            {
                return Hud.IsUserHidden();
            }
            catch (Exception)
            {
                return false;
            }
        }
    }
}
