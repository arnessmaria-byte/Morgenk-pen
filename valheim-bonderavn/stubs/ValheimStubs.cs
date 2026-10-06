// STUBBER. Speiler bare signaturene BondeRavn bruker fra assembly_valheim.dll.
// Verdiene her er dummy; den ekte logikken ligger i spillet.
// Hold denne fila i synk med det BondeRavn faktisk kaller.

using System;
using System.Collections.Generic;
using UnityEngine;

public class ZDOID { }

public class ZDO
{
    public float GetFloat(string name, float defaultValue = 0f) => defaultValue;
    public int GetInt(string name, int defaultValue = 0) => defaultValue;
    public long GetLong(string name, long defaultValue = 0L) => defaultValue;
    public string GetString(string name, string defaultValue = "") => defaultValue;
    public bool GetBool(string name, bool defaultValue = false) => defaultValue;
}

public class ZNetView : MonoBehaviour
{
    public static bool m_forceDisableInit;
    public bool IsValid() => false;
    public bool IsOwner() => false;
    public ZDO GetZDO() => null;
}

public class ZNet : MonoBehaviour
{
    public static ZNet instance;
    public DateTime GetTime() => DateTime.UtcNow;
}

public class ZNetScene : MonoBehaviour
{
    public static ZNetScene instance;
    public GameObject GetPrefab(string name) => null;
    public string GetPrefabName(GameObject go) => go ? go.name : "";
}

public class Localization
{
    public static Localization instance;
    public string Localize(string text) => text;
}

public class Hud : MonoBehaviour
{
    public static Hud instance;
    public static bool IsUserHidden() => false;
}

public class MessageHud : MonoBehaviour
{
    public static MessageHud instance;
    public enum MessageType { TopLeft = 1, Center = 2 }
    public void ShowMessage(MessageType type, string text, int amount = 0, Sprite icon = null) { }
}

public class ItemDrop : MonoBehaviour
{
    [Serializable]
    public class ItemData
    {
        [Serializable]
        public class SharedData
        {
            public string m_name = "";
        }
        public SharedData m_shared = new SharedData();
    }
    public ItemData m_itemData = new ItemData();
}

public class Character : MonoBehaviour
{
    public string m_name = "";
    private static readonly List<Character> s_characters = new List<Character>();
    public static List<Character> GetAllCharacters() => s_characters;
    public int GetLevel() => 1;
    public bool IsTamed() => false;
    public bool IsDead() => false;
    public bool IsPlayer() => false;
    public string GetHoverName() => m_name;
    public Vector3 GetHeadPoint() => transform.position;
    public Vector3 GetLookDir() => transform.forward;
    public bool InInterior() => false;
    public bool IsTeleporting() => false;
}

public class Player : Character
{
    public static Player m_localPlayer;
}

public class BaseAI : MonoBehaviour
{
    public bool IsAlerted() => false;
}

public class MonsterAI : BaseAI
{
    public List<ItemDrop> m_consumeItems = new List<ItemDrop>();
    public float m_consumeRange = 2f;
}

public class Tameable : MonoBehaviour
{
    public float m_fedDuration = 30f;
    public float m_tamingTime = 1800f;
    public bool m_commandable;
    public bool IsTamed() => false;
    public bool IsHungry() => false;
}

public class Procreation : MonoBehaviour
{
    public float m_updateInterval = 10f;
    public float m_totalCheckRange = 10f;
    public int m_maxCreatures = 4;
    public float m_partnerCheckRange = 3f;
    public float m_pregnancyChance = 0.5f;
    public float m_pregnancyDuration = 10f;
    public int m_requiredLovePoints = 4;
    public GameObject m_offspring;
    public int m_minOffspringLevel;
    public bool IsPregnant() => false;
    public bool IsDue() => false;
}

public class Growup : MonoBehaviour
{
    public float m_growTime = 60f;
    public GameObject m_grownPrefab;
}

public class Plant : MonoBehaviour
{
    public enum Status { Healthy, NoSun, NoSpace, WrongBiome, NotCultivated, TooCold, TooHot }
    public string m_name = "";
    public float m_growTime = 100f;
    public float m_growTimeMax = 200f;
    public Status m_status;
    private double TimeSincePlanted() => 0;
    private float GetGrowTime() => m_growTime;
}
