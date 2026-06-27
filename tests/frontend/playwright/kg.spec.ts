import { test, expect } from '@playwright/test';

test('kg page renders and returns rows', async ({ page }) => {
  // 1. الانتقال إلى صفحة الـ KG (تأكد من المسار الصحيح، غالباً /kg)
  await page.goto('/kg');

  // 2. إذا كان هناك نموذج بحث، قم بتعبئته
  // await page.fill('input[name="query"]', 'ginger');
  // await page.click('button[type="submit"]');

  // 3. انتظر ظهور النتائج (استخدم محددًا CSS يظهر في الجدول بعد تحميل البيانات)
  // سنفترض وجود عنصر يحمل الكلاس 'result-row' أو جدول
  await expect(page.locator('.result-row').first()).toBeVisible({ timeout: 10000 });

  // 4. تأكد من أن هناك صفوفاً على الأقل (أكبر من 0)
  const rows = page.locator('.result-row');
  await expect(rows.count()).toBeGreaterThan(0);
});