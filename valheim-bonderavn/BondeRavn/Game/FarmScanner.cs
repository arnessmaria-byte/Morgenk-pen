using System;
using System.Collections.Generic;
using BondeRavn.Coach;
using UnityEngine;

namespace BondeRavn.Game
{
    /// <summary>
    /// Leser av spillets tilstand (dyr, temming, avl, planter) rundt spilleren
    /// og pakker det i en FarmReport som CoachBrain forstår.
    /// </summary>
    internal static class FarmScanner
    {
        private sealed class Row
        {
            public AnimalInfo Info;
            public Vector3 Pos;
            public bool Procreates;
            public bool ReadyForPartner;
        }

        public static FarmReport Scan(Player player, float radius, bool includePlants, float plantRadius)
        {
            var report = new FarmReport { NowSeconds = Time.unscaledTime };
            if (player == null) return report;

            Vector3 playerPos = player.transform.position;
            DateTime now = GameAccess.GameTime();

            var rows = new List<Row>();
            List<Character> all;
            try
            {
                all = Character.GetAllCharacters();
            }
            catch (Exception)
            {
                return report;
            }

            foreach (var c in all)
            {
                if (c == null) continue;
                Row row = ReadAnimal(c, playerPos, now);
                if (row != null) rows.Add(row);
            }

            ComputeNeighbours(rows);

            float r2 = radius * radius;
            foreach (var row in rows)
            {
                if ((row.Pos - playerPos).sqrMagnitude <= r2)
                    report.Animals.Add(row.Info);
            }

            if (includePlants)
                ScanPlants(report, playerPos, plantRadius);

            return report;
        }

        private static Row ReadAnimal(Character c, Vector3 playerPos, DateTime now)
        {
            try
            {
                if (c is Player || c.IsPlayer() || c.IsDead()) return null;

                var tameable = c.GetComponent<Tameable>();
                var growup = c.GetComponent<Growup>();
                if (tameable == null && growup == null) return null;

                var a = new AnimalInfo
                {
                    Id = c.GetInstanceID(),
                    Prefab = GameAccess.PrefabName(c.gameObject),
                    Species = GameAccess.Localize(c.m_name),
                    Level = Mathf.Clamp(c.GetLevel(), 1, 3),
                    Tamed = c.IsTamed(),
                };

                Vector3 pos = c.transform.position;
                a.X = pos.x; a.Y = pos.y; a.Z = pos.z;
                a.DistanceToPlayer = Vector3.Distance(playerPos, pos);

                var zdo = GameAccess.ZdoOf(c);
                if (zdo != null)
                {
                    try { a.PetName = zdo.GetString(GameAccess.Keys.TamedName, "") ?? ""; }
                    catch (Exception) { a.PetName = ""; }
                }

                var ai = c.GetComponent<BaseAI>();
                if (ai != null)
                {
                    a.Alerted = ai.IsAlerted();
                    var monster = ai as MonsterAI;
                    if (monster != null && monster.m_consumeItems != null)
                    {
                        foreach (var item in monster.m_consumeItems)
                        {
                            if (item == null || item.m_itemData == null || item.m_itemData.m_shared == null) continue;
                            string name = GameAccess.Localize(item.m_itemData.m_shared.m_name);
                            if (!string.IsNullOrEmpty(name) && !a.Foods.Contains(name)) a.Foods.Add(name);
                        }
                    }
                }

                if (tameable != null)
                {
                    a.Tameable = true;
                    a.Hungry = tameable.IsHungry();
                    a.TamingTotalSec = tameable.m_tamingTime;
                    a.FedDurationSec = tameable.m_fedDuration;
                    a.TamingLeftSec = tameable.m_tamingTime;
                    if (zdo != null)
                    {
                        try { a.TamingLeftSec = zdo.GetFloat(GameAccess.Keys.TameTimeLeft, tameable.m_tamingTime); }
                        catch (Exception) { }
                    }
                    if (a.Tamed) a.TamingLeftSec = 0f;
                }

                var proc = c.GetComponent<Procreation>();
                if (proc != null)
                {
                    a.CanProcreate = true;
                    a.RequiredLovePoints = proc.m_requiredLovePoints;
                    a.MaxCreatures = proc.m_maxCreatures;
                    a.TotalCheckRange = proc.m_totalCheckRange;
                    a.PartnerCheckRange = proc.m_partnerCheckRange;
                    a.PregnancyChance = proc.m_pregnancyChance;
                    a.PregnancyDurationSec = proc.m_pregnancyDuration;
                    a.ProcreationIntervalSec = proc.m_updateInterval;
                    a.MinOffspringLevel = proc.m_minOffspringLevel;
                    a.Pregnant = proc.IsPregnant();

                    if (zdo != null)
                    {
                        try { a.LovePoints = zdo.GetInt(GameAccess.Keys.LovePoints, 0); }
                        catch (Exception) { }

                        if (a.Pregnant)
                        {
                            try
                            {
                                long ticks = zdo.GetLong(GameAccess.Keys.Pregnant, 0L);
                                if (ticks > 0)
                                {
                                    double elapsed = (now - new DateTime(ticks)).TotalSeconds;
                                    a.DueInSec = Mathf.Max(0f, proc.m_pregnancyDuration - (float)elapsed);
                                }
                                else a.DueInSec = proc.m_pregnancyDuration;
                            }
                            catch (Exception) { a.DueInSec = proc.m_pregnancyDuration; }
                        }
                    }
                }

                if (growup != null)
                {
                    a.IsYoung = true;
                    a.GrowUpInSec = growup.m_growTime;
                    if (zdo != null)
                    {
                        try
                        {
                            long ticks = zdo.GetLong(GameAccess.Keys.SpawnTime, now.Ticks);
                            double elapsed = (now - new DateTime(ticks)).TotalSeconds;
                            a.GrowUpInSec = Mathf.Max(0f, growup.m_growTime - (float)elapsed);
                        }
                        catch (Exception) { }
                    }
                }

                return new Row
                {
                    Info = a,
                    Pos = pos,
                    Procreates = proc != null,
                    ReadyForPartner = a.Tamed && proc != null && !a.Pregnant && !a.Hungry,
                };
            }
            catch (Exception ex)
            {
                BondeRavnPlugin.Log.LogDebug("Klarte ikke lese dyr: " + ex.Message);
                return null;
            }
        }

        /// <summary>
        /// Etterligner spillets egen telling (SpawnSystem.GetNrOfInstances): navnet på prefaben brukes
        /// som prefiks, så "Boar_piggy" teller som "Boar" når grensen for antall sjekkes.
        /// </summary>
        private static void ComputeNeighbours(List<Row> rows)
        {
            foreach (var me in rows)
            {
                if (!me.Procreates) continue;
                var a = me.Info;
                float total2 = a.TotalCheckRange * a.TotalCheckRange;
                float partner2 = a.PartnerCheckRange * a.PartnerCheckRange;
                int sameKind = 0;
                int partners = 0;

                foreach (var other in rows)
                {
                    if (!other.Info.Prefab.StartsWith(a.Prefab, StringComparison.Ordinal)) continue;
                    float d2 = (other.Pos - me.Pos).sqrMagnitude;
                    if (d2 <= total2) sameKind++;
                    if (other != me && other.ReadyForPartner && other.Info.Prefab == a.Prefab && d2 <= partner2) partners++;
                }

                a.SameKindWithinTotalRange = sameKind;
                a.PartnersWithinPartnerRange = partners;
            }
        }

        private static void ScanPlants(FarmReport report, Vector3 playerPos, float radius)
        {
            Plant[] plants;
            try
            {
                plants = UnityEngine.Object.FindObjectsOfType<Plant>();
            }
            catch (Exception)
            {
                return;
            }

            float r2 = radius * radius;
            foreach (var p in plants)
            {
                if (p == null) continue;
                if ((p.transform.position - playerPos).sqrMagnitude > r2) continue;
                report.Plants.Add(new PlantInfo
                {
                    Name = GameAccess.PlantDisplayName(p),
                    Status = GameAccess.PlantStatusName(p),
                    ReadyInSec = GameAccess.PlantReadyInSeconds(p),
                });
            }
        }
    }
}
