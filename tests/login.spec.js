// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Page de connexion', () => {

  test('Affiche le formulaire de connexion', async ({ page }) => {
    await page.goto('/login/');
    await expect(page.getByRole('heading', { name: 'Stark Todo-List' })).toBeVisible();
    await expect(page.getByText('Connectez-vous pour accéder à vos protocoles')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Se connecter' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Créer un compte' })).toBeVisible();
  });

  test('Redirige vers la page d\'inscription via le lien', async ({ page }) => {
    await page.goto('/login/');
    await page.getByRole('link', { name: 'Créer un compte' }).click();
    await expect(page).toHaveURL(/.*register/);
  });

  test('Connecte un utilisateur valide et redirige vers le Kanban', async ({ page }) => {
    const user = `LoginTest_${Date.now()}`;

    await page.goto('/register/');
    await page.locator('#id_username').fill(user);
    await page.locator('#id_password1').fill('StrongPass2026!');
    await page.locator('#id_password2').fill('StrongPass2026!');
    await page.getByRole('button', { name: "S'inscrire et démarrer" }).click();
    await expect(page).toHaveURL('/');

    await page.getByRole('button', { name: 'Déconnexion' }).click();

    await page.goto('/login/');
    await page.locator('#id_username').fill(user);
    await page.locator('#id_password').fill('StrongPass2026!');
    await page.getByRole('button', { name: 'Se connecter' }).click();

    await expect(page).toHaveURL('/');
    await expect(page.getByRole('heading', { name: new RegExp(`Bonjour, ${user}`, 'i') })).toBeVisible();
  });
});
