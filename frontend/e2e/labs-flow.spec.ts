import { test, expect } from '@playwright/test';

test.describe('Labs Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Accept disclaimer first
    await page.goto('/disclaimer');
    await page.locator('input[type="checkbox"]').first().check();
    await page.locator('input[type="checkbox"]').last().check();
    await page.locator('button:has-text("I Understand")').click();
    await page.waitForURL(/\/home/);
  });

  test('should show labs page with patient form', async ({ page }) => {
    await page.goto('/labs');

    await expect(page.locator('h1')).toContainText('Lab');
    await expect(page.locator('label:has-text("Age")')).toBeVisible();
    await expect(page.locator('label:has-text("Sex")')).toBeVisible();
  });

  test('should navigate to lab input after filling patient info', async ({ page }) => {
    await page.goto('/labs');

    // Fill patient info
    await page.locator('input[type="number"]').fill('45');
    await page.locator('select').selectOption('male');

    await page.locator('button:has-text("Continue")').click();
    await expect(page).toHaveURL(/\/labs\/input/);
  });

  test('should show lab test options grouped by category', async ({ page }) => {
    await page.goto('/labs');
    await page.locator('input[type="number"]').fill('45');
    await page.locator('select').selectOption('male');
    await page.locator('button:has-text("Continue")').click();

    await page.waitForURL(/\/labs\/input/);

    // Check for lab categories in dropdown
    const labSelect = page.locator('select').first();
    await labSelect.click();

    // Should have optgroups for categories
    await expect(page.locator('optgroup[label="Cardiac"]')).toBeVisible();
    await expect(page.locator('optgroup[label="Hematology"]')).toBeVisible();
    await expect(page.locator('optgroup[label="Electrolytes"]')).toBeVisible();
  });

  test('should allow adding lab results', async ({ page }) => {
    await page.goto('/labs');
    await page.locator('input[type="number"]').fill('45');
    await page.locator('select').first().selectOption('male');
    await page.locator('button:has-text("Continue")').click();

    await page.waitForURL(/\/labs\/input/);

    // Add a lab result
    await page.locator('select').first().selectOption('troponin');
    await page.locator('input[placeholder="Enter value"]').fill('50');
    await page.locator('button:has-text("Add Lab Result")').click();

    // Should show the added lab
    await expect(page.locator('text=Troponin')).toBeVisible();
    await expect(page.locator('text=50')).toBeVisible();
  });

  test('should allow removing added labs', async ({ page }) => {
    await page.goto('/labs');
    await page.locator('input[type="number"]').fill('45');
    await page.locator('select').first().selectOption('male');
    await page.locator('button:has-text("Continue")').click();

    await page.waitForURL(/\/labs\/input/);

    // Add a lab
    await page.locator('input[placeholder="Enter value"]').fill('50');
    await page.locator('button:has-text("Add Lab Result")').click();

    // Remove it
    await page.locator('button:has-text("Remove")').click();

    // Should no longer show the lab value in the list
    await expect(page.locator('.bg-gray-50:has-text("50")')).not.toBeVisible();
  });
});
