using System;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using BondeRavn.Coach;
using BondeRavn.Game;
using UnityEngine;

namespace BondeRavn
{
    /// <summary>
    /// BondeRavn: en ravn som følger deg i Valheim, leser av gården din og coacher deg
    /// på temming og avl (høyest mulig stjerner), pluss litt planteråd.
    /// Ingen Harmony-patcher: modden bare leser spilltilstand, den endrer ingenting.
    /// </summary>
    [BepInPlugin(Guid, Name, Version)]
    public sealed class BondeRavnPlugin : BaseUnityPlugin
    {
        public const string Guid = "no.morgenkapen.bonderavn";
        public const string Name = "BondeRavn";
        public const string Version = "0.1.0";

        internal static ManualLogSource Log;

        private ConfigEntry<bool> _enabled;
        private ConfigEntry<string> _ravenName;
        private ConfigEntry<float> _scanRadius;
        private ConfigEntry<float> _scanInterval;
        private ConfigEntry<float> _tipInterval;
        private ConfigEntry<float> _repeatCooldown;
        private ConfigEntry<bool> _chatter;
        private ConfigEntry<bool> _plants;
        private ConfigEntry<float> _plantRadius;
        private ConfigEntry<bool> _showRaven;
        private ConfigEntry<float> _ravenScale;
        private ConfigEntry<float> _offsetX, _offsetY, _offsetZ;
        private ConfigEntry<bool> _showBoard;
        private ConfigEntry<bool> _eventsInHud;
        private ConfigEntry<float> _bubbleX, _bubbleY, _bubbleWidth;
        private ConfigEntry<int> _fontSize;
        private ConfigEntry<KeyboardShortcut> _keyToggle;
        private ConfigEntry<KeyboardShortcut> _keyBoard;
        private ConfigEntry<KeyboardShortcut> _keyAsk;

        private CoachBrain _brain;
        private RavnHud _hud;
        private RavnCompanion _raven;
        private FarmReport _lastReport;
        private float _nextScan;
        private bool _greeted;
        private string _lastLine;

        private void Awake()
        {
            Log = Logger;

            _enabled = Config.Bind("1. Generelt", "Aktiv", true, "Slå hele ravnen av eller på.");
            _ravenName = Config.Bind("1. Generelt", "Navn", "Ravn", "Hva ravnen heter i snakkebobla.");
            _chatter = Config.Bind("1. Generelt", "Småprat", true, "La ravnen småprate når det ikke er noe å rapportere.");
            _eventsInHud = Config.Bind("1. Generelt", "HendelserISpillHud", true, "Vis hendelser (ny tam, gravid, født) også i spillets egen meldingsstripe.");

            _scanRadius = Config.Bind("2. Coach", "Skanneradius", 48f, new ConfigDescription("Hvor langt fra deg ravnen leser dyr (meter).", new AcceptableValueRange<float>(8f, 200f)));
            _scanInterval = Config.Bind("2. Coach", "Skanneintervall", 4f, new ConfigDescription("Sekunder mellom hver avlesning av spillet.", new AcceptableValueRange<float>(1f, 60f)));
            _tipInterval = Config.Bind("2. Coach", "RådIntervall", 14f, new ConfigDescription("Sekunder hvert råd står før neste.", new AcceptableValueRange<float>(3f, 120f)));
            _repeatCooldown = Config.Bind("2. Coach", "GjentaTidligst", 90f, new ConfigDescription("Sekunder før samme råd gjentas.", new AcceptableValueRange<float>(10f, 900f)));
            _plants = Config.Bind("2. Coach", "Planteråd", true, "Ta med planter (for tett, feil biom, klare til høsting).");
            _plantRadius = Config.Bind("2. Coach", "Planteradius", 30f, new ConfigDescription("Hvor langt fra deg planter leses (meter).", new AcceptableValueRange<float>(5f, 100f)));

            _showRaven = Config.Bind("3. Ravn", "VisRavn", true, "Vis selve ravnen som flyr ved skulderen din.");
            _ravenScale = Config.Bind("3. Ravn", "Størrelse", 0.7f, new ConfigDescription("Skalering av ravnemodellen.", new AcceptableValueRange<float>(0.2f, 2f)));
            _offsetX = Config.Bind("3. Ravn", "PosisjonSide", -0.75f, "Avstand til siden (negativ = venstre skulder).");
            _offsetY = Config.Bind("3. Ravn", "PosisjonOpp", 0.55f, "Høyde over hodet.");
            _offsetZ = Config.Bind("3. Ravn", "PosisjonFram", -0.25f, "Avstand foran (negativ = bak).");

            _showBoard = Config.Bind("4. HUD", "VisTavle", false, "Vis oversiktstavle over dyrene i nærheten.");
            _bubbleX = Config.Bind("4. HUD", "BobleX", 0.02f, new ConfigDescription("Vannrett plassering (andel av skjermbredde).", new AcceptableValueRange<float>(0f, 0.9f)));
            _bubbleY = Config.Bind("4. HUD", "BobleY", 0.28f, new ConfigDescription("Loddrett plassering (andel av skjermhøyde).", new AcceptableValueRange<float>(0f, 0.9f)));
            _bubbleWidth = Config.Bind("4. HUD", "BobleBredde", 430f, new ConfigDescription("Bredde på bobla i piksler.", new AcceptableValueRange<float>(200f, 1200f)));
            _fontSize = Config.Bind("4. HUD", "Skriftstørrelse", 16, new ConfigDescription("Skriftstørrelse i bobla.", new AcceptableValueRange<int>(10, 36)));

            _keyToggle = Config.Bind("5. Taster", "SlåAvPå", new KeyboardShortcut(KeyCode.F7), "Slå ravnen av eller på.");
            _keyBoard = Config.Bind("5. Taster", "Tavle", new KeyboardShortcut(KeyCode.F8), "Vis eller skjul oversiktstavla.");
            _keyAsk = Config.Bind("5. Taster", "SpørRavnen", new KeyboardShortcut(KeyCode.F9), "Be ravnen om det viktigste rådet akkurat nå.");

            _brain = new CoachBrain();
            ApplyBrainConfig();

            _hud = gameObject.AddComponent<RavnHud>();
            ApplyHudConfig();

            Config.SettingChanged += (s, e) =>
            {
                ApplyBrainConfig();
                ApplyHudConfig();
                if (_raven != null)
                {
                    _raven.Scale = _ravenScale.Value;
                    _raven.Offset = new Vector3(_offsetX.Value, _offsetY.Value, _offsetZ.Value);
                    _raven.transform.localScale = Vector3.one * _ravenScale.Value;
                }
            };

            Log.LogInfo(Name + " " + Version + " lastet. Krra.");
        }

        private void ApplyBrainConfig()
        {
            _brain.TipIntervalSec = _tipInterval.Value;
            _brain.RepeatCooldownSec = _repeatCooldown.Value;
            _brain.Chatter = _chatter.Value;
        }

        private void ApplyHudConfig()
        {
            _hud.RavenName = _ravenName.Value;
            _hud.AnchorX = _bubbleX.Value;
            _hud.AnchorY = _bubbleY.Value;
            _hud.Width = _bubbleWidth.Value;
            _hud.FontSize = _fontSize.Value;
            _hud.ShowBoard = _showBoard.Value;
        }

        private void Update()
        {
            HandleKeys();

            var player = Player.m_localPlayer;
            if (player == null || !_enabled.Value)
            {
                Despawn();
                _hud.Line = null;
                _hud.Board = null;
                _greeted = false;
                return;
            }

            if (_showRaven.Value && _raven == null)
            {
                _raven = RavnCompanion.Spawn(_ravenScale.Value, new Vector3(_offsetX.Value, _offsetY.Value, _offsetZ.Value));
            }
            else if (!_showRaven.Value && _raven != null)
            {
                Despawn();
            }

            float now = Time.unscaledTime;
            if (!_greeted)
            {
                _greeted = true;
                _brain.Say("Krra! " + _ravenName.Value + " her. Jeg flyr med deg og passer på fjøset. " + _keyBoard.Value + " gir deg tavla, " + _keyAsk.Value + " spør meg.", now);
                _nextScan = 0f;
            }

            if (now >= _nextScan)
            {
                _nextScan = now + _scanInterval.Value;
                try
                {
                    _lastReport = FarmScanner.Scan(player, _scanRadius.Value, _plants.Value, _plantRadius.Value);
                    _brain.Analyze(_lastReport);
                    _hud.Board = _brain.BuildBoard(_lastReport);
                }
                catch (Exception ex)
                {
                    Log.LogWarning("Skanning feilet: " + ex);
                }
            }

            string line = _brain.Speak(now);
            if (!ReferenceEquals(line, _lastLine))
            {
                _lastLine = line;
                if (!string.IsNullOrEmpty(line))
                {
                    if (_raven != null) _raven.Hop();
                    if (_eventsInHud.Value && _brain.CurrentIsEvent)
                        GameAccess.TryShowHudMessage(_ravenName.Value + ": " + line, false);
                }
            }
            _hud.Line = line;
        }

        private void HandleKeys()
        {
            if (_keyToggle.Value.IsDown())
            {
                _enabled.Value = !_enabled.Value;
                Log.LogInfo(_enabled.Value ? "Ravnen er på." : "Ravnen er av.");
            }
            if (_keyBoard.Value.IsDown())
            {
                _showBoard.Value = !_showBoard.Value;
                _hud.ShowBoard = _showBoard.Value;
            }
            if (_keyAsk.Value.IsDown() && _enabled.Value)
            {
                _nextScan = 0f;
                var tips = _brain.CurrentTips;
                if (tips.Count > 0) _brain.Say(tips[0].Text, Time.unscaledTime);
                else _brain.Say("Ingenting å melde. Gå nærmere dyrene dine, så ser jeg bedre.", Time.unscaledTime);
            }
        }

        private void Despawn()
        {
            if (_raven == null) return;
            Destroy(_raven.gameObject);
            _raven = null;
        }

        private void OnDestroy()
        {
            Despawn();
        }
    }
}
