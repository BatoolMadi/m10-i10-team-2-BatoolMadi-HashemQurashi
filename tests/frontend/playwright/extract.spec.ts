import { test, expect } from '@playwright/test';

test('extract page renders and returns entities', async ({ page }) => {
  // 1. Navigate to the extract page
  await page.goto('/extract');

  // 2. Verify the input field is visible (replace 'textarea' with the correct selector)
  const input = page.locator('textarea[name="recipe-text"]');
  await expect(input).toBeVisible();

  // 3. Enter sample text
  await input.fill('Mix flour, sugar, and eggs to make a cake.');

  // 4. Click the extract button
  await page.click('button[type="submit"]');

  // 5. Wait for results (from the API)
  // Assume results are shown in a list or element with class 'entity-item'
  const entityResult = page.locator('.entity-item');
  await expect(entityResult.first()).toBeVisible({ timeout: 10000 });

  // 6. Verify API content appears on the page
  const text = await entityResult.first().textContent();
  expect(text).not.toBeNull();
});
