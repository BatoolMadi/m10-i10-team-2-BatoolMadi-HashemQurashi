import { test, expect } from '@playwright/test';

test('rag page renders cited answer', async ({ page }) => {
  // 1. الانتقال إلى صفحة الـ RAG
  await page.goto('/rag');

  // 2. إدخال السؤال في حقل النص (استبدل 'input[name="question"]' بالمعرف الفعلي عندك)
  await page.fill('input[name="question"]', 'Find Sichuan recipes that use ginger');
  
  // 3. النقر على زر الإرسال
  await page.click('button[type="submit"]');

  // 4. الانتظار حتى ظهور الإجابة في الصفحة
  // افترضنا أن الإجابة تظهر داخل عنصر له الكلاس 'answer-text'
  const answerLocator = page.locator('.answer-text');
  await expect(answerLocator).toBeVisible({ timeout: 20000 }); // زيادة التوقيت لأن الـ AI قد يأخذ وقتاً

  // 5. التحقق من أن النص يحتوي على مراجع بصيغة [1] أو [N]
  const answerText = await answerLocator.textContent();
  expect(answerText).toMatch(/\[\d+\]/); // هذا تعبير نمطي (Regex) يبحث عن [رقم]
});