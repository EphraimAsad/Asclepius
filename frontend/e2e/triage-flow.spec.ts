import { test, expect } from '@playwright/test';

test.describe('Triage Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Accept disclaimer first
    await page.goto('/disclaimer');
    await page.locator('input[type="checkbox"]').first().check();
    await page.locator('input[type="checkbox"]').last().check();
    await page.locator('button:has-text("I Understand")').click();
    await page.waitForURL(/\/home/);
  });

  test('should show chief complaint selection', async ({ page }) => {
    await page.goto('/triage');

    await expect(page.locator('h1')).toContainText('symptom');
    await expect(page.locator('text=Chest Pain')).toBeVisible();
    await expect(page.locator('text=Headache')).toBeVisible();
  });

  test('should show all 21 chief complaints', async ({ page }) => {
    await page.goto('/triage');

    // Check for some of the complaints
    await expect(page.locator('text=Chest Pain')).toBeVisible();
    await expect(page.locator('text=Shortness of Breath')).toBeVisible();
    await expect(page.locator('text=Abdominal Pain')).toBeVisible();
    await expect(page.locator('text=Dizziness')).toBeVisible();
    await expect(page.locator('text=Fever')).toBeVisible();
    await expect(page.locator('text=Back Pain')).toBeVisible();
    await expect(page.locator('text=Leg Swelling')).toBeVisible();
  });

  test('should navigate to symptoms page after selecting complaint', async ({ page }) => {
    await page.goto('/triage');

    await page.locator('text=Chest Pain').click();
    await page.locator('button:has-text("Continue")').click();

    await expect(page).toHaveURL(/\/triage\/symptoms/);
  });

  test('should show symptom checkboxes relevant to complaint', async ({ page }) => {
    await page.goto('/triage');

    await page.locator('text=Chest Pain').click();
    await page.locator('button:has-text("Continue")').click();

    await page.waitForURL(/\/triage\/symptoms/);

    // Should show chest pain specific symptoms
    await expect(page.locator('text=Pressure, squeezing')).toBeVisible();
    await expect(page.locator('text=Shortness of breath')).toBeVisible();
  });

  test('should show emergency warning symptoms', async ({ page }) => {
    await page.goto('/triage');

    await page.locator('text=Chest Pain').click();
    await page.locator('button:has-text("Continue")').click();

    await page.waitForURL(/\/triage\/symptoms/);

    // Should show emergency section
    await expect(page.locator('text=Emergency Warning Signs')).toBeVisible();
    await expect(page.locator('text=Person is unresponsive')).toBeVisible();
  });

  test('should complete full triage flow', async ({ page }) => {
    await page.goto('/triage');

    // Select complaint
    await page.locator('text=Chest Pain').click();
    await page.locator('button:has-text("Continue")').click();

    // Select symptoms
    await page.waitForURL(/\/triage\/symptoms/);
    await page.locator('text=Pressure, squeezing').click();
    await page.locator('button:has-text("Review")').click();

    // Review page
    await page.waitForURL(/\/triage\/review/);
    await expect(page.locator('text=Review')).toBeVisible();
  });
});
