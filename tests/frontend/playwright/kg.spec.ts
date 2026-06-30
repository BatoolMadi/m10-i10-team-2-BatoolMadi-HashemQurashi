import { test, expect } from '@playwright/test';

test('kg page renders and returns rows', async ({ page }) => {
  // 1. Navigate to the KG page (confirm the path, usually /kg)
  await page.goto('/kg');

  // 2. If there is a search form, fill it in
  // await page.fill('input[name="query"]', 'ginger');
  // await page.click('button[type="submit"]');

  // 3. Wait for results (use a CSS selector that appears in the table after data loads)
  // Assume an element with class 'result-row' or a table
  await expect(page.locator('.result-row').first()).toBeVisible({ timeout: 10000 });

  // 4. Ensure at least one row exists
  const rows = page.locator('.result-row');
  await expect(rows.count()).toBeGreaterThan(0);
});
