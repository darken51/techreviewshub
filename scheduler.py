#!/usr/bin/env python3
"""
🤖 SCHEDULER AUTOMATIQUE
Planifie l'exécution automatique de tâches
"""

import schedule
import time
import subprocess
from datetime import datetime

class TaskScheduler:
    """Planificateur de tâches automatiques"""

    def __init__(self):
        self.tasks_run = 0

    def generate_new_reviews(self):
        """Génère de nouvelles reviews automatiquement"""
        print(f"\n🤖 [{datetime.now()}] Génération automatique de reviews...")

        try:
            result = subprocess.run(
                ['python3', 'automate_all.py'],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print("✅ Reviews générées avec succès")
                self.tasks_run += 1
            else:
                print(f"❌ Erreur: {result.stderr}")

        except subprocess.TimeoutExpired:
            print("⏱️  Timeout - processus trop long")
        except Exception as e:
            print(f"❌ Erreur: {e}")

    def update_prices(self):
        """Met à jour les prix automatiquement"""
        print(f"\n💰 [{datetime.now()}] Mise à jour automatique des prix...")

        try:
            result = subprocess.run(
                ['python3', 'auto_price_updater.py'],
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode == 0:
                print("✅ Prix mis à jour")
                self.tasks_run += 1
            else:
                print(f"❌ Erreur: {result.stderr}")

        except Exception as e:
            print(f"❌ Erreur: {e}")

    def backup_site(self):
        """Crée un backup automatique du site"""
        print(f"\n💾 [{datetime.now()}] Backup automatique...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}.tar.gz"

        try:
            subprocess.run(
                ['tar', '-czf', backup_name, '--exclude=backup_*.tar.gz', '.'],
                check=True
            )
            print(f"✅ Backup créé: {backup_name}")
            self.tasks_run += 1
        except Exception as e:
            print(f"❌ Erreur backup: {e}")

    def cleanup_old_backups(self):
        """Supprime les anciens backups (garde les 7 derniers)"""
        print(f"\n🧹 [{datetime.now()}] Nettoyage des anciens backups...")

        try:
            import glob
            backups = sorted(glob.glob('backup_*.tar.gz'))

            if len(backups) > 7:
                to_delete = backups[:-7]
                for backup in to_delete:
                    subprocess.run(['rm', backup])
                    print(f"  🗑️  Supprimé: {backup}")
                print(f"✅ {len(to_delete)} anciens backups supprimés")
            else:
                print("⏺️  Aucun backup à supprimer")

        except Exception as e:
            print(f"❌ Erreur: {e}")

    def health_check(self):
        """Vérifie la santé du site"""
        print(f"\n🏥 [{datetime.now()}] Health check...")

        checks = {
            'index.html exists': lambda: subprocess.run(['test', '-f', 'index.html']).returncode == 0,
            'reviews count > 20': lambda: len(subprocess.run(['ls', '-1'], capture_output=True, text=True).stdout.split('\n')) > 20,
            'git repo ok': lambda: subprocess.run(['git', 'status'], capture_output=True).returncode == 0
        }

        all_ok = True
        for name, check in checks.items():
            try:
                if check():
                    print(f"  ✅ {name}")
                else:
                    print(f"  ❌ {name}")
                    all_ok = False
            except:
                print(f"  ❌ {name} (error)")
                all_ok = False

        if all_ok:
            print("✅ Tout est OK")
        else:
            print("⚠️  Problèmes détectés")

    def setup_schedule(self):
        """Configure le planning des tâches"""
        print("🤖 CONFIGURATION DU SCHEDULER")
        print("="*60)

        # Génération de reviews: tous les lundis à 2h
        schedule.every().monday.at("02:00").do(self.generate_new_reviews)
        print("✅ Reviews: chaque lundi 2h")

        # Mise à jour prix: tous les jours à 3h
        schedule.every().day.at("03:00").do(self.update_prices)
        print("✅ Prix: chaque jour 3h")

        # Backup: tous les jours à 4h
        schedule.every().day.at("04:00").do(self.backup_site)
        print("✅ Backup: chaque jour 4h")

        # Nettoyage: tous les dimanches à 5h
        schedule.every().sunday.at("05:00").do(self.cleanup_old_backups)
        print("✅ Nettoyage: chaque dimanche 5h")

        # Health check: toutes les 6 heures
        schedule.every(6).hours.do(self.health_check)
        print("✅ Health check: toutes les 6h")

        print("\n💡 Scheduler configuré - en attente...")

    def run(self):
        """Démarre le scheduler"""
        self.setup_schedule()

        print(f"\n⏰ Démarrage: {datetime.now()}")
        print("Appuyez sur Ctrl+C pour arrêter\n")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check toutes les minutes

        except KeyboardInterrupt:
            print(f"\n\n⏹️  Arrêt du scheduler")
            print(f"Tâches exécutées: {self.tasks_run}")
            print(f"Durée: {datetime.now()}")


def setup_cron_job():
    """Aide à configurer un cron job système"""
    print("\n📋 CONFIGURATION CRON JOB")
    print("="*60)
    print("\nPour automatiser complètement, ajoutez ces lignes à votre crontab:")
    print("\n# Éditer le crontab:")
    print("  crontab -e")
    print("\n# Ajouter ces lignes:")
    print("""
# Tech Reviews Hub - Génération automatique reviews (lundis 2h)
0 2 * * 1 cd /home/fred/techreviewshub-site && python3 automate_all.py >> /tmp/reviews_cron.log 2>&1

# Tech Reviews Hub - Mise à jour prix (tous les jours 3h)
0 3 * * * cd /home/fred/techreviewshub-site && python3 auto_price_updater.py >> /tmp/prices_cron.log 2>&1

# Tech Reviews Hub - Backup (tous les jours 4h)
0 4 * * * cd /home/fred/techreviewshub-site && tar -czf backup_$(date +%Y%m%d).tar.gz . >> /tmp/backup_cron.log 2>&1
""")
    print("\n💾 Sauvegarder et quitter (ESC puis :wq dans vim)")
    print("\n📊 Voir les logs:")
    print("  tail -f /tmp/reviews_cron.log")
    print("  tail -f /tmp/prices_cron.log")


def main():
    """Point d'entrée"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--cron-help':
        setup_cron_job()
        return

    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("🧪 MODE TEST - Exécution immédiate de toutes les tâches\n")
        scheduler = TaskScheduler()
        scheduler.health_check()
        print("\n✅ Test terminé")
        return

    print("🤖 SCHEDULER TECH REVIEWS HUB")
    print("="*60)
    print("\nOptions:")
    print("  python3 scheduler.py              # Démarre le scheduler")
    print("  python3 scheduler.py --test       # Test des tâches")
    print("  python3 scheduler.py --cron-help  # Aide cron job")
    print()

    choice = input("Démarrer le scheduler maintenant? (o/n): ")

    if choice.lower() == 'o':
        scheduler = TaskScheduler()
        scheduler.run()
    else:
        print("\n💡 Pour démarrer plus tard:")
        print("  python3 scheduler.py")


if __name__ == "__main__":
    # Installer schedule si nécessaire
    try:
        import schedule
    except ImportError:
        print("📦 Installation de 'schedule'...")
        subprocess.run(['pip3', 'install', 'schedule'])
        import schedule

    main()
