using System;
using System.Collections.Generic;
using UnityEngine;

namespace BondeRavn.Game
{
    /// <summary>
    /// Selve ravnen: en lokal (ikke nettverkssynkronisert) kopi av spillets ravnemodell
    /// som svever ved skulderen til spilleren, som feen i Zelda.
    /// Finnes ikke modellen, bygges en enkel ravn av primitiver.
    /// </summary>
    internal sealed class RavnCompanion : MonoBehaviour
    {
        private static readonly string[] PrefabCandidates = { "Raven", "Hugin", "Munin", "Crow" };

        public Vector3 Offset = new Vector3(-0.75f, 0.55f, -0.25f);
        public float Scale = 0.7f;

        private Vector3 _velocity;
        private float _bobSeed;
        private float _hopUntil;
        private Animator _animator;
        private Transform _leftWing, _rightWing;
        private readonly List<Renderer> _renderers = new List<Renderer>();
        private bool _visible = true;

        public static RavnCompanion Spawn(float scale, Vector3 offset)
        {
            GameObject go = BuildFromGamePrefab() ?? BuildPrimitive();
            go.name = "BondeRavn";
            var comp = go.AddComponent<RavnCompanion>();
            comp.Scale = scale;
            comp.Offset = offset;
            go.transform.localScale = Vector3.one * scale;
            comp._bobSeed = UnityEngine.Random.Range(0f, 10f);
            comp.GetComponentsInChildren(true, comp._renderers);
            comp._animator = go.GetComponentInChildren<Animator>();
            comp.TrySetFlying();

            var p = Player.m_localPlayer;
            if (p != null) go.transform.position = p.GetHeadPoint() + Vector3.up;
            return comp;
        }

        public void Hop()
        {
            _hopUntil = Time.time + 0.6f;
        }

        public void SetVisible(bool visible)
        {
            if (_visible == visible) return;
            _visible = visible;
            foreach (var r in _renderers) if (r != null) r.enabled = visible;
        }

        private void LateUpdate()
        {
            var p = Player.m_localPlayer;
            if (p == null)
            {
                Destroy(gameObject);
                return;
            }

            bool hide = false;
            try { hide = p.IsDead() || p.IsTeleporting(); }
            catch (Exception) { }
            SetVisible(!hide);

            Transform pt = p.transform;
            Vector3 anchor;
            try { anchor = p.GetHeadPoint(); }
            catch (Exception) { anchor = pt.position + Vector3.up * 1.6f; }

            float t = Time.time + _bobSeed;
            float bob = Mathf.Sin(t * 2.1f) * 0.07f + Mathf.Sin(t * 0.7f) * 0.04f;
            float sway = Mathf.Sin(t * 0.9f) * 0.08f;
            Vector3 target = anchor
                             + pt.right * (Offset.x + sway)
                             + Vector3.up * (Offset.y + bob)
                             + pt.forward * Offset.z;

            if (Time.time < _hopUntil)
            {
                float k = 1f - (_hopUntil - Time.time) / 0.6f;
                target += Vector3.up * Mathf.Sin(k * Mathf.PI) * 0.35f;
            }

            if ((transform.position - target).sqrMagnitude > 20f * 20f)
            {
                transform.position = target;
                _velocity = Vector3.zero;
            }
            else
            {
                transform.position = Vector3.SmoothDamp(transform.position, target, ref _velocity, 0.22f, 30f);
            }

            Vector3 look = Vector3.zero;
            try { look = p.GetLookDir(); }
            catch (Exception) { }
            look.y = 0f;
            if (look.sqrMagnitude < 0.01f) look = pt.forward;
            Quaternion want = Quaternion.LookRotation(look.normalized, Vector3.up);
            want *= Quaternion.Euler(0f, -12f, Mathf.Sin(t * 1.3f) * 4f);
            transform.rotation = Quaternion.Slerp(transform.rotation, want, Time.deltaTime * 5f);

            if (_leftWing != null && _rightWing != null)
            {
                float flap = Mathf.Sin(t * 9f) * 28f;
                _leftWing.localRotation = Quaternion.Euler(0f, 0f, 20f + flap);
                _rightWing.localRotation = Quaternion.Euler(0f, 0f, -20f - flap);
            }
        }

        private void TrySetFlying()
        {
            if (_animator == null) return;
            try
            {
                _animator.applyRootMotion = false;
                _animator.cullingMode = AnimatorCullingMode.AlwaysAnimate;
                foreach (var prm in _animator.parameters)
                {
                    if (prm.type == AnimatorControllerParameterType.Bool &&
                        (prm.name == "flying" || prm.name == "Flying" || prm.name == "fly"))
                    {
                        _animator.SetBool(prm.name, true);
                    }
                }
            }
            catch (Exception)
            {
                // Animatoren er ikke kritisk; modellen står stille om dette feiler.
            }
        }

        // ------------------------------------------------------------------
        // Bygging av modellen
        // ------------------------------------------------------------------

        private static GameObject BuildFromGamePrefab()
        {
            try
            {
                var scene = ZNetScene.instance;
                if (scene == null) return null;

                GameObject prefab = null;
                foreach (var name in PrefabCandidates)
                {
                    prefab = scene.GetPrefab(name);
                    if (prefab != null) break;
                }
                if (prefab == null) return null;

                // Lag kopien deaktivert så ingen Awake() rekker å registrere den i nettverket,
                // fjern all spillogikk, og slå den på igjen som ren pynt.
                bool wasActive = prefab.activeSelf;
                prefab.SetActive(false);
                GameObject clone;
                try
                {
                    clone = UnityEngine.Object.Instantiate(prefab);
                }
                finally
                {
                    prefab.SetActive(wasActive);
                }

                StripGameLogic(clone);
                clone.SetActive(true);
                return clone;
            }
            catch (Exception ex)
            {
                BondeRavnPlugin.Log.LogWarning("Fikk ikke brukt spillets ravnemodell, bygger en enkel ravn i stedet: " + ex.Message);
                return null;
            }
        }

        private static void StripGameLogic(GameObject root)
        {
            // Flere runder, fordi noen komponenter nekter å forsvinne før de som avhenger av dem er borte.
            for (int pass = 0; pass < 6; pass++)
            {
                bool removedAny = false;
                foreach (var mb in root.GetComponentsInChildren<MonoBehaviour>(true))
                {
                    if (mb == null) continue;
                    try
                    {
                        UnityEngine.Object.DestroyImmediate(mb);
                        removedAny = true;
                    }
                    catch (Exception) { }
                }
                foreach (var col in root.GetComponentsInChildren<Collider>(true))
                {
                    try { UnityEngine.Object.DestroyImmediate(col); removedAny = true; } catch (Exception) { }
                }
                foreach (var rb in root.GetComponentsInChildren<Rigidbody>(true))
                {
                    try { UnityEngine.Object.DestroyImmediate(rb); removedAny = true; } catch (Exception) { }
                }
                foreach (var audio in root.GetComponentsInChildren<AudioSource>(true))
                {
                    try { UnityEngine.Object.DestroyImmediate(audio); removedAny = true; } catch (Exception) { }
                }
                if (!removedAny) break;
            }

            // Alle underobjekter skal være synlige (noen prefaber har skjulte varianter).
            foreach (var tr in root.GetComponentsInChildren<Transform>(true))
            {
                if (tr != root.transform && tr.name.ToLowerInvariant().Contains("visual")) tr.gameObject.SetActive(true);
            }
        }

        private static GameObject BuildPrimitive()
        {
            var root = new GameObject("BondeRavn_primitiv");
            Material black = MakeMaterial(new Color(0.08f, 0.08f, 0.1f));
            Material beak = MakeMaterial(new Color(0.85f, 0.6f, 0.2f));
            Material eye = MakeMaterial(new Color(0.9f, 0.85f, 0.4f));

            AddPart(root.transform, PrimitiveType.Sphere, "kropp", new Vector3(0f, 0f, 0f), new Vector3(0.26f, 0.22f, 0.42f), black);
            AddPart(root.transform, PrimitiveType.Sphere, "hode", new Vector3(0f, 0.14f, 0.2f), new Vector3(0.17f, 0.17f, 0.17f), black);
            AddPart(root.transform, PrimitiveType.Cube, "nebb", new Vector3(0f, 0.12f, 0.32f), new Vector3(0.05f, 0.04f, 0.14f), beak);
            AddPart(root.transform, PrimitiveType.Sphere, "øye_v", new Vector3(-0.06f, 0.17f, 0.26f), new Vector3(0.035f, 0.035f, 0.035f), eye);
            AddPart(root.transform, PrimitiveType.Sphere, "øye_h", new Vector3(0.06f, 0.17f, 0.26f), new Vector3(0.035f, 0.035f, 0.035f), eye);
            AddPart(root.transform, PrimitiveType.Cube, "hale", new Vector3(0f, 0.02f, -0.28f), new Vector3(0.12f, 0.02f, 0.2f), black);

            var left = new GameObject("vinge_v").transform;
            left.SetParent(root.transform, false);
            left.localPosition = new Vector3(-0.1f, 0.06f, 0f);
            AddPart(left, PrimitiveType.Cube, "fjær", new Vector3(-0.22f, 0f, 0f), new Vector3(0.44f, 0.02f, 0.2f), black);

            var right = new GameObject("vinge_h").transform;
            right.SetParent(root.transform, false);
            right.localPosition = new Vector3(0.1f, 0.06f, 0f);
            AddPart(right, PrimitiveType.Cube, "fjær", new Vector3(0.22f, 0f, 0f), new Vector3(0.44f, 0.02f, 0.2f), black);

            var comp = root.AddComponent<WingTag>();
            comp.Left = left;
            comp.Right = right;
            return root;
        }

        private sealed class WingTag : MonoBehaviour
        {
            public Transform Left, Right;
        }

        private void Awake()
        {
            var wings = GetComponent<WingTag>();
            if (wings != null)
            {
                _leftWing = wings.Left;
                _rightWing = wings.Right;
            }
        }

        private static void AddPart(Transform parent, PrimitiveType type, string name, Vector3 pos, Vector3 scale, Material mat)
        {
            var go = GameObject.CreatePrimitive(type);
            go.name = name;
            var col = go.GetComponent<Collider>();
            if (col != null) UnityEngine.Object.DestroyImmediate(col);
            go.transform.SetParent(parent, false);
            go.transform.localPosition = pos;
            go.transform.localScale = scale;
            var r = go.GetComponent<Renderer>();
            if (r != null && mat != null) r.sharedMaterial = mat;
        }

        private static Material MakeMaterial(Color color)
        {
            Shader shader = Shader.Find("Standard")
                            ?? Shader.Find("Legacy Shaders/Diffuse")
                            ?? Shader.Find("Unlit/Color")
                            ?? Shader.Find("Sprites/Default");
            if (shader == null) return null;
            var m = new Material(shader) { color = color };
            return m;
        }
    }
}
