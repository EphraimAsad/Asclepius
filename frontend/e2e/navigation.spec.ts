import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test.beforeEach(async ({ page }) => {
    // Accept disclaimer first
    await page.goto('/disclaimer');
    await page.locator('input[type="checkbox"]').first().check();
    await page.locator('input[type="checkbox"]').last().check();
    await page.locator('button:has-text("I Understand")').click();
    await page.waitForURL(/\/home/);
  });

  test('should display home page with navigation options', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Asclepius');
    await expect(page.locator('text=Symptom Check')).toBeVisible();
    await expect(page.locator('text=Lab Results')).toBeVisible();
  });

  test('should navigate to triage from home', async ({ page }) => {
    await page.locator('text=Symptom Check').click();
    await expect(page).toHaveURL(/\/triage/);
  });

  test('should navigate to labs from home', async ({ page }) => {
    await page.locator('text=Lab Results').click();
    await expect(page).toHaveURL(/\/labs/);
  });

  test('should have working header navigation', async ({ page }) => {
    // Navigate to triage
    await page.goto('/triage');

    // Click logo/home link if present
    const homeLink = page.locator('header a[href="/home"]');
    if (await homeLink.isVisible()) {
      await homeLink.click();
      await expect(page).toHaveURL(/\/home/);
    }
  });
});
