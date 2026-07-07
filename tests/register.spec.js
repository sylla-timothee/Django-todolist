// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Page d\'inscription', () => {

  test('Affiche le formulaire d\'inscription', async ({ page }) => {
    await page.goto('/register/');
    await expect(page.getByRole('heading', { name: 'Créer un compte' })).toBeVisible();
    await expect(page.getByText('Rejoignez le système pour sécuriser vos tâches')).toBeVisible();
    await expect(page.getByRole('button', { name: "S'inscrire et démarrer" })).toBeVisible();
  });

  test('Permet à un nouvel utilisateur de s\'inscrire', async ({ page }) => {
    const user = `Inscription_${Date.now()}`;
    await page.goto('/register/');
    await page.locator('#id_username').fill(user);
    await page.locator('#id_password1').fill('StarkIndustry2026!');
    await page.locator('#id_password2').fill('StarkIndustry2026!');
    await page.getByRole('button', { name: "S'inscrire et démarrer" }).click();

    await expect(page).toHaveURL('/');
    await expect(page.getByRole('heading', { name: new RegExp(`Bonjour, ${user}`, 'i') })).toBeVisible();
  });

  test('Redirige vers la page de connexion via le lien du bas', async ({ page }) => {
    await page.goto('/register/');
    await page.getByRole('link', { name: 'Connectez-vous ici' }).click();
    await expect(page).toHaveURL(/.*login/);
  });

  test('Affiche les erreurs pour un mot de passe trop court', async ({ page }) => {
    await page.goto('/register/');
    await page.locator('#id_username').fill('UserFaible');
    await page.locator('#id_password1').fill('ab');
    await page.locator('#id_password2').fill('ab');
    await page.getByRole('button', { name: "S'inscrire et démarrer" }).click();

    await expect(page.locator('.text-red-500')).toBeVisible();
    await expect(page).toHaveURL(/.*register/);
  });
});
