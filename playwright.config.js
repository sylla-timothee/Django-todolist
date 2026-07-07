// @ts-check
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: 'html',
  timeout: 30000,
  use: {
    baseURL: 'http://127.0.0.1:8000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: './env/bin/python manage.py migrate && ./env/bin/python manage.py runserver 0.0.0.0:8000',
    url: 'http://127.0.0.1:8000/login/',
    reuseExistingServer: true,
    timeout: 30000,
  },
});
