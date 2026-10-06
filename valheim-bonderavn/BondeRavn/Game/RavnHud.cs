using UnityEngine;

namespace BondeRavn.Game
{
    /// <summary>
    /// Snakkebobla til ravnen og den valgfrie oversiktstavla, tegnet med IMGUI.
    /// </summary>
    internal sealed class RavnHud : MonoBehaviour
    {
        public string RavenName = "Ravn";
        public string Line;
        public string Board;
        public bool ShowBoard;
        public float AnchorX = 0.02f;
        public float AnchorY = 0.28f;
        public float Width = 430f;
        public int FontSize = 16;

        private GUIStyle _bubble, _title, _text, _board;
        private Texture2D _bg, _bgBoard;
        private float _lineChangedAt;
        private string _lastLine;

        private void OnGUI()
        {
            if (Player.m_localPlayer == null) return;
            if (GameAccess.HudHidden()) return;
            if (string.IsNullOrEmpty(Line) && !(ShowBoard && !string.IsNullOrEmpty(Board))) return;

            EnsureStyles();

            float x = Screen.width * AnchorX;
            float y = Screen.height * AnchorY;

            if (!string.IsNullOrEmpty(Line))
            {
                if (!ReferenceEquals(Line, _lastLine))
                {
                    _lastLine = Line;
                    _lineChangedAt = Time.unscaledTime;
                }
                float pop = Mathf.Clamp01((Time.unscaledTime - _lineChangedAt) / 0.18f);
                float w = Width * Mathf.Lerp(0.9f, 1f, pop);

                GUIContent content = new GUIContent(Line);
                float textH = _text.CalcHeight(content, w - 24f);
                float h = textH + 40f;

                GUI.Box(new Rect(x, y, w, h), GUIContent.none, _bubble);
                GUI.Label(new Rect(x + 12f, y + 6f, w - 24f, 22f), RavenName, _title);
                GUI.Label(new Rect(x + 12f, y + 28f, w - 24f, textH + 4f), content, _text);
                y += h + 8f;
            }

            if (ShowBoard && !string.IsNullOrEmpty(Board))
            {
                GUIContent content = new GUIContent(Board);
                float w = Width;
                float textH = _board.CalcHeight(content, w - 24f);
                GUI.Box(new Rect(x, y, w, textH + 36f), GUIContent.none, _bubble);
                GUI.Label(new Rect(x + 12f, y + 6f, w - 24f, 22f), "Gården", _title);
                GUI.Label(new Rect(x + 12f, y + 28f, w - 24f, textH + 4f), content, _board);
            }
        }

        private void EnsureStyles()
        {
            if (_bubble != null && _text.fontSize == FontSize) return;

            if (_bg == null) _bg = Solid(new Color(0.07f, 0.06f, 0.05f, 0.82f));
            if (_bgBoard == null) _bgBoard = Solid(new Color(0.05f, 0.07f, 0.06f, 0.78f));

            _bubble = new GUIStyle(GUI.skin.box);
            _bubble.normal.background = _bg;
            _bubble.border = new RectOffset(4, 4, 4, 4);

            _title = new GUIStyle(GUI.skin.label)
            {
                fontSize = FontSize,
                fontStyle = FontStyle.Bold,
                alignment = TextAnchor.UpperLeft,
            };
            _title.normal.textColor = new Color(0.95f, 0.78f, 0.35f);

            _text = new GUIStyle(GUI.skin.label)
            {
                fontSize = FontSize,
                wordWrap = true,
                alignment = TextAnchor.UpperLeft,
                richText = false,
            };
            _text.normal.textColor = new Color(0.96f, 0.94f, 0.88f);

            _board = new GUIStyle(_text) { fontSize = Mathf.Max(10, FontSize - 2) };
            _board.normal.textColor = new Color(0.85f, 0.9f, 0.82f);
        }

        private static Texture2D Solid(Color c)
        {
            var t = new Texture2D(1, 1, TextureFormat.RGBA32, false);
            t.SetPixel(0, 0, c);
            t.Apply();
            return t;
        }
    }
}
