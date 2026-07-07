// @ts-check
import { test, expect } from '@playwright/test';

const TEST_USER = `KanbanUser_${Date.now()}`;
const TEST_PASS = 'StrongPass2026!';

test.describe('Kanban — CRUD, Drag & Drop et Accessibilité', () => {

  test.beforeEach(async ({ page }) => {
    const user = `${TEST_USER}_${Math.random().toString(36).slice(2, 8)}`;
    await page.goto('/register/');
    await page.locator('#id_username').fill(user);
    await page.locator('#id_password1').fill(TEST_PASS);
    await page.locator('#id_password2').fill(TEST_PASS);
    await page.getByRole('button', { name: "S'inscrire et démarrer" }).click();
    await expect(page).toHaveURL('/');
  });

  function counterBadge(column) {
    return column.locator('h3 .rounded-full.ml-auto');
  }

  test('Crée une tâche et la voit apparaître dans la colonne "À faire"', async ({ page }) => {
    await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
    await expect(page).toHaveURL(/.*task-create/);

    await page.locator('#id_title').fill('Tâche de test E2E');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();
    await expect(page).toHaveURL('/');

    const todoColumn = page.locator('.kanban-column[data-status="todo"]');
    await expect(todoColumn.locator('.task-card')).toHaveCount(1);
    await expect(todoColumn.locator('.task-card')).toContainText('Tâche de test E2E');
    await expect(counterBadge(todoColumn)).toHaveText('1');
  });

  test('Crée plusieurs tâches et vérifie leur répartition', async ({ page }) => {
    for (const titre of ['Première tâche', 'Deuxième tâche']) {
      await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
      await page.locator('#id_title').fill(titre);
      await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();
      await expect(page).toHaveURL('/');
    }

    const todoColumn = page.locator('.kanban-column[data-status="todo"]');
    await expect(todoColumn.locator('.task-card')).toHaveCount(2);
    await expect(counterBadge(todoColumn)).toHaveText('2');
  });

  test('Modifie le titre d\'une tâche', async ({ page }) => {
    await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
    await page.locator('#id_title').fill('Titre original');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();
    await expect(page).toHaveURL('/');

    await page.locator('.task-card a').filter({ hasText: 'Modifier' }).click();
    await expect(page).toHaveURL(/.*task-update/);

    await page.locator('#id_title').fill('Titre modifié');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();

    await expect(page).toHaveURL('/');
    await expect(page.locator('.task-card')).toContainText('Titre modifié');
  });

  test('Supprime une tâche', async ({ page }) => {
    await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
    await page.locator('#id_title').fill('Tâche à supprimer');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();
    await expect(page).toHaveURL('/');
    await expect(page.locator('.task-card')).toHaveCount(1);

    await page.locator('.task-card a').filter({ hasText: 'Supprimer' }).click();
    await expect(page).toHaveURL(/.*task-delete/);

    await page.getByRole('button', { name: 'Confirmer la suppression' }).click();
    await expect(page).toHaveURL('/');

    await expect(page.locator('.task-card')).toHaveCount(0);
  });

  test('Déplace une tâche de "À faire" vers "En cours" via l\'API', async ({ page }) => {
    await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
    await page.locator('#id_title').fill('Tâche à déplacer');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();
    await expect(page).toHaveURL('/');

    const taskId = await page.locator('.task-card').getAttribute('data-id');
    expect(taskId).toBeTruthy();

    const csrfToken = await page.evaluate(() => {
      const match = document.cookie.match(/csrftoken=([^;]+)/);
      return match ? match[1] : '';
    });

    const response = await page.evaluate(async ({ id, token }) => {
      const res = await fetch('/api/update-task-status/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token },
        body: JSON.stringify({ id, status: 'in_progress' }),
      });
      return res.json();
    }, { id: Number(taskId), token: csrfToken });

    expect(response.success).toBe(true);

    await page.reload();

    const inProgressColumn = page.locator('.kanban-column[data-status="in_progress"]');
    await expect(inProgressColumn.locator('.task-card')).toHaveCount(1);
    await expect(inProgressColumn.locator('.task-card')).toContainText('Tâche à déplacer');
    await expect(counterBadge(inProgressColumn)).toHaveText('1');

    const todoColumn = page.locator('.kanban-column[data-status="todo"]');
    await expect(todoColumn.locator('.task-card')).toHaveCount(0);
    await expect(counterBadge(todoColumn)).toHaveText('0');
  });

  test('Déplace une tâche à travers les trois colonnes', async ({ page }) => {
    await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
    await page.locator('#id_title').fill('Voyageuse');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();
    await expect(page).toHaveURL('/');

    const taskId = await page.locator('.task-card').getAttribute('data-id');

    const csrfToken = await page.evaluate(() => {
      const match = document.cookie.match(/csrftoken=([^;]+)/);
      return match ? match[1] : '';
    });

    async function deplacer(id, status) {
      const r = await page.evaluate(async ({ id, status, token }) => {
        const res = await fetch('/api/update-task-status/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token },
          body: JSON.stringify({ id, status }),
        });
        return res.json();
      }, { id, status, token: csrfToken });
      expect(r.success).toBe(true);
    }

    await deplacer(Number(taskId), 'in_progress');
    await page.reload();
    await expect(page.locator('.kanban-column[data-status="in_progress"] .task-card')).toHaveCount(1);

    await deplacer(Number(taskId), 'done');
    await page.reload();
    await expect(page.locator('.kanban-column[data-status="done"] .task-card')).toHaveCount(1);

    await deplacer(Number(taskId), 'todo');
    await page.reload();
    await expect(page.locator('.kanban-column[data-status="todo"] .task-card')).toHaveCount(1);
  });

  test('Les cartes sont focus au clavier (tabindex="0")', async ({ page }) => {
    await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
    await page.locator('#id_title').fill('Carte focusable');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();
    await expect(page).toHaveURL('/');

    const card = page.locator('.task-card');
    await expect(card).toHaveAttribute('tabindex', '0');
    await expect(card).toHaveAttribute('role', 'listitem');
    await expect(card).toHaveAttribute('aria-label');

    for (let i = 0; i < 4; i++) {
      await page.keyboard.press('Tab');
      const isFocused = await card.evaluate(el => el === document.activeElement);
      if (isFocused) break;
    }
    await expect(card).toBeFocused();
  });

  test('Les boutons Modifier et Supprimer sont accessibles au clavier', async ({ page }) => {
    await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
    await page.locator('#id_title').fill('Tâche clavier');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();
    await expect(page).toHaveURL('/');

    const card = page.locator('.task-card');
    for (let i = 0; i < 4; i++) {
      await page.keyboard.press('Tab');
      const isFocused = await card.evaluate(el => el === document.activeElement);
      if (isFocused) break;
    }

    await page.keyboard.press('Tab');
    const modifyLink = page.locator('.task-card a').filter({ hasText: 'Modifier' });
    await expect(modifyLink).toBeFocused();

    await page.keyboard.press('Tab');
    const deleteLink = page.locator('.task-card a').filter({ hasText: 'Supprimer' });
    await expect(deleteLink).toBeFocused();
  });

  test('Affiche le statut actuel dans le formulaire d\'édition', async ({ page }) => {
    await page.getByRole('link', { name: 'Nouvelle Tâche' }).click();
    await page.locator('#id_title').fill('Tâche avec statut');
    await page.getByRole('button', { name: 'Confirmer et enregistrer' }).click();

    await page.locator('.task-card a').filter({ hasText: 'Modifier' }).click();
    await expect(page.locator('text=Statut actuel')).toBeVisible();
    await expect(page.locator('text=À faire')).toBeVisible();
  });
});
