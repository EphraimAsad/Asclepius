import { test, expect } from '@playwright/test';

test.describe('Disclaimer Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Clear localStorage before each test
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
  });

  test('should redirect to disclaimer when no consent', async ({ page }) => {
    await page.goto('/home');
    await expect(page).toHaveURL(/\/disclaimer/);
  });

  test('should display disclaimer page correctly', async ({ page }) => {
    await page.goto('/disclaimer');

    // Check for key elements
    await expect(page.locator('h1')).toContainText('Important');
    await expect(page.locator('text=NOT a substitute')).toBeVisible();
    await expect(page.locator('text=18 years')).toBeVisible();
    await expect(page.locator('button:has-text("I Understand")')).toBeVisible();
  });

  test('should enable continue button only after checking both boxes', async ({ page }) => {
    await page.goto('/disclaimer');

    const continueButton = page.locator('button:has-text("I Understand")');

    // Button should be disabled initially
    await expect(continueButton).toBeDisabled();

    // Check first checkbox
    await page.locator('input[type="checkbox"]').first().check();
    await expect(continueButton).toBeDisabled();

    // Check second checkbox
    await page.locator('input[type="checkbox"]').last().check();
    await expect(continueButton).toBeEnabled();
  });

  test('should navigate to home after accepting disclaimer', async ({ page }) => {
    await page.goto('/disclaimer');

    // Accept disclaimer
    await page.locator('input[type="checkbox"]').first().check();
    await page.locator('input[type="checkbox"]').last().check();
    await page.locator('button:has-text("I Understand")').click();

    // Should redirect to home
    await expect(page).toHaveURL(/\/home/);
  });

  test('should persist consent across page navigation', async ({ page }) => {
    await page.goto('/disclaimer');

    // Accept disclaimer
    await page.locator('input[type="checkbox"]').first().check();
    await page.locator('input[type="checkbox"]').last().check();
    await page.locator('button:has-text("I Understand")').click();

    // Navigate away and back
    await page.goto('/triage');
    await expect(page).not.toHaveURL(/\/disclaimer/);
  });
});
