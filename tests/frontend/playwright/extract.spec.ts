import { test, expect } from '@playwright/test';

test('extract page renders and returns entities', async ({ page }) => {
  // 1. الانتقال إلى صفحة الاستخراج
  await page.goto('/extract');

  // 2. التحقق من وجود حقل الإدخال (استبدل 'textarea' بالـ selector الصحيح عندك)
  const input = page.locator('textarea[name="recipe-text"]');
  await expect(input).toBeVisible();

  // 3. إدخال نص تجريبي
  await input.fill('Mix flour, sugar, and eggs to make a cake.');

  // 4. الضغط على زر الاستخراج
  await page.click('button[type="submit"]');

  // 5. انتظار ظهور النتائج (التي ستأتي من الـ API)
  // نفترض أنك تعرض النتائج في قائمة أو عنصر يحتوي على كلاس 'entity-item'
  const entityResult = page.locator('.entity-item');
  await expect(entityResult.first()).toBeVisible({ timeout: 10000 });

  // 6. التحقق من أن محتوى الـ API يظهر في الصفحة
  const text = await entityResult.first().textContent();
  expect(text).not.toBeNull();
});