// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Page Kanban — Liste des tâches', () => {

  test.beforeEach(async ({ page }) => {
    const user = `KanbanView_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
    await page.goto('/register/');
    await page.locator('#id_username').fill(user);
    await page.locator('#id_password1').fill('TestPass123!');
    await page.locator('#id_password2').fill('TestPass123!');
    await page.getByRole('button', { name: "S'inscrire et démarrer" }).click();
    await expect(page).toHaveURL('/');
  });

  test('Affiche les éléments d\'en-tête (message de bienvenue et Déconnexion)', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /Bonjour,/i })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Déconnexion' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Tableau de bord' })).toBeVisible();
  });

  test('Affiche les trois colonnes Kanban', async ({ page }) => {
    const colonnes = page.locator('.kanban-column');
    await expect(colonnes).toHaveCount(3);
    await expect(colonnes.nth(0).locator('h3')).toContainText('À faire');
    await expect(colonnes.nth(1).locator('h3')).toContainText('En cours');
    await expect(colonnes.nth(2).locator('h3')).toContainText('Terminé');
  });

  test('Affiche les compteurs à zéro pour un nouvel utilisateur', async ({ page }) => {
    const compteurs = page.locator('.kanban-column h3 .rounded-full.ml-auto');
    await expect(compteurs).toHaveCount(3);
    await expect(compteurs.nth(0)).toHaveText('0');
    await expect(compteurs.nth(1)).toHaveText('0');
    await expect(compteurs.nth(2)).toHaveText('0');
  });

  test('Affiche le message "Aucune tâche" dans chaque colonne vide', async ({ page }) => {
    const messages = page.locator('.kanban-column [role="status"]');
    await expect(messages).toHaveCount(3);
    for (const message of await messages.all()) {
      await expect(message).toContainText('Aucune tâche');
    }
  });

  test('Le bouton Nouvelle Tâche redirige vers la création', async ({ page }) => {
    const bouton = page.getByRole('link', { name: 'Nouvelle Tâche' });
    await expect(bouton).toBeVisible();
    await bouton.click();
    await expect(page).toHaveURL(/.*task-create/);
  });

  test('Permet de se déconnecter', async ({ page }) => {
    await page.getByRole('button', { name: 'Déconnexion' }).click();
    await expect(page).toHaveURL(/.*login/);
  });

  test('Les colonnes ont les attributs aria-label', async ({ page }) => {
    await expect(page.locator('[aria-label="Colonne À faire"]')).toBeVisible();
    await expect(page.locator('[aria-label="Colonne En cours"]')).toBeVisible();
    await expect(page.locator('[aria-label="Colonne Terminé"]')).toBeVisible();
  });

  test('La région aria-live est présente', async ({ page }) => {
    await expect(page.locator('#sr-announcement[aria-live="polite"]')).toBeVisible();
  });

  test('Le tableau a role="region" avec aria-label', async ({ page }) => {
    await expect(page.locator('[role="region"][aria-label="Tableau des tâches"]')).toBeVisible();
  });
});
