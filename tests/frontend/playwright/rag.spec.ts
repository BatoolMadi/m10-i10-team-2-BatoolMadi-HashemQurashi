import { test, expect } from '@playwright/test';

test('rag page renders cited answer', async ({ page }) => {
  // 1. Navigate to the RAG page
  await page.goto('/rag');

  // 2. Enter the question in the text field (replace 'input[name="question"]' with the actual id)
  await page.fill('input[name="question"]', 'Find Sichuan recipes that use ginger');

  // 3. Click the submit button
  await page.click('button[type="submit"]');

  // 4. Wait until the answer appears on the page
  // Assume the answer appears inside an element with class 'answer-text'
  const answerLocator = page.locator('.answer-text');
  await expect(answerLocator).toBeVisible({ timeout: 20000 }); // longer timeout because AI may take time

  // 5. Verify the text contains citation markers like [1] or [N]
  const answerText = await answerLocator.textContent();
  expect(answerText).toMatch(/\[\d+\]/); // regex looking for [digit]
});
