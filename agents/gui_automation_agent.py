"""
GUI Automation Agent - Generates Selenium TypeScript test automation code.
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .agent_prompts import get_agent_prompt
from loguru import logger


class GUIAutomationAgent(BaseAgent):
    """GUI Automation Agent that generates Selenium-based test automation code."""
    
    def __init__(self):
        super().__init__(
            name="GUI Automation Agent",
            role="Generate Selenium TypeScript-based GUI test automation",
            temperature=0.7
        )
    
    def get_system_prompt(self) -> str:
        """Get system prompt for GUI automation."""
        return get_agent_prompt('gui_automation')
    
    def execute_task(self, task: Dict, context: Optional[str] = None) -> Dict:
        """
        Execute GUI automation task.
        
        Args:
            task: Task dictionary
            context: Optional context
            
        Returns:
            Task result
        """
        test_cases = task.get('test_cases', [])
        framework = task.get('framework', {})
        
        return self.generate_gui_automation(test_cases, framework, context)
    
    def generate_gui_automation(self,
                                test_cases: List[Dict],
                                framework: Dict,
                                context: Optional[str] = None) -> Dict:
        """
        Generate GUI automation code in TypeScript.
        
        Args:
            test_cases: GUI test cases
            framework: Framework design
            context: Additional context
            
        Returns:
            Generated automation code
        """
        logger.info("Generating GUI automation code (Selenium + TypeScript)...")
        
        prompt = f"""
Generate complete Selenium-based GUI test automation code in TypeScript based on:

TEST CASES:
{test_cases}

FRAMEWORK DESIGN:
{framework}

CONTEXT:
{context}

Generate the following files with complete, executable TypeScript code:

1. frontend/pages/base_page.ts
```typescript
// Base Page Object class
// Include:
// - WebDriver instance management
// - Common page methods
// - Wait utilities
// - Screenshot capture
// - Navigation methods
// - Element interaction methods

import {{ WebDriver, By, until, WebElement }} from 'selenium-webdriver';

export class BasePage {{
    protected driver: WebDriver;
    protected baseUrl: string;
    protected timeout: number = 10000;

    constructor(driver: WebDriver, baseUrl: string) {{
        this.driver = driver;
        this.baseUrl = baseUrl;
    }}

    async navigate(path: string = ''): Promise<void> {{
        await this.driver.get(`${this.baseUrl}${path}`);
    }}

    async findElement(locator: By): Promise<WebElement> {{
        await this.driver.wait(until.elementLocated(locator), this.timeout);
        return this.driver.findElement(locator);
    }}

    async findElements(locator: By): Promise<WebElement[]> {{
        await this.driver.wait(until.elementLocated(locator), this.timeout);
        return this.driver.findElements(locator);
    }}

    async click(locator: By): Promise<void> {{
        const element = await this.findElement(locator);
        await this.driver.wait(until.elementIsVisible(element), this.timeout);
        await this.driver.wait(until.elementIsEnabled(element), this.timeout);
        await element.click();
    }}

    async type(locator: By, text: string, clearFirst: boolean = true): Promise<void> {{
        const element = await this.findElement(locator);
        if (clearFirst) {{
            await element.clear();
        }}
        await element.sendKeys(text);
    }}

    async getText(locator: By): Promise<string> {{
        const element = await this.findElement(locator);
        return element.getText();
    }}

    async isDisplayed(locator: By): Promise<boolean> {{
        try {{
            const element = await this.driver.findElement(locator);
            return element.isDisplayed();
        }} catch {{
            return false;
        }}
    }}

    async waitForElement(locator: By, timeout?: number): Promise<void> {{
        await this.driver.wait(
            until.elementLocated(locator),
            timeout || this.timeout
        );
    }}

    async takeScreenshot(filename: string): Promise<void> {{
        const screenshot = await this.driver.takeScreenshot();
        // Save screenshot logic
    }}

    async getCurrentUrl(): Promise<string> {{
        return this.driver.getCurrentUrl();
    }}

    async getPageTitle(): Promise<string> {{
        return this.driver.getTitle();
    }}
}}
```

2. frontend/pages/login_page.ts
```typescript
// Example Page Object implementation
// Create similar page objects for each page

import {{ WebDriver, By }} from 'selenium-webdriver';
import {{ BasePage }} from './base_page';

export class LoginPage extends BasePage {{
    // Locators
    private usernameInput = By.id('username');
    private passwordInput = By.id('password');
    private loginButton = By.css('button[type="submit"]');
    private errorMessage = By.className('error-message');

    constructor(driver: WebDriver, baseUrl: string) {{
        super(driver, baseUrl);
    }}

    async navigate(): Promise<void> {{
        await super.navigate('/login');
    }}

    async login(username: string, password: string): Promise<void> {{
        await this.type(this.usernameInput, username);
        await this.type(this.passwordInput, password);
        await this.click(this.loginButton);
    }}

    async getErrorMessage(): Promise<string> {{
        return this.getText(this.errorMessage);
    }}

    async isLoginButtonEnabled(): Promise<boolean> {{
        const button = await this.findElement(this.loginButton);
        return button.isEnabled();
    }}
}}
```

3. frontend/tests/login.test.ts
```typescript
// Complete test file implementing ALL GUI test cases
// Use Jest framework

import {{ WebDriver, Builder }} from 'selenium-webdriver';
import {{ LoginPage }} from '../pages/login_page';
import {{ config }} from '../config/test_config';

describe('Login Tests', () => {{
    let driver: WebDriver;
    let loginPage: LoginPage;

    beforeAll(async () => {{
        driver = await new Builder()
            .forBrowser('chrome')
            .build();
    }});

    afterAll(async () => {{
        await driver.quit();
    }});

    beforeEach(async () => {{
        loginPage = new LoginPage(driver, config.baseUrl);
        await loginPage.navigate();
    }});

    test('should login successfully with valid credentials', async () => {{
        await loginPage.login('testuser', 'password123');
        const currentUrl = await loginPage.getCurrentUrl();
        expect(currentUrl).toContain('/dashboard');
    }});

    test('should show error with invalid credentials', async () => {{
        await loginPage.login('invalid', 'wrong');
        const errorMsg = await loginPage.getErrorMessage();
        expect(errorMsg).toContain('Invalid credentials');
    }});

    test('should disable login button with empty fields', async () => {{
        const isEnabled = await loginPage.isLoginButtonEnabled();
        expect(isEnabled).toBe(false);
    }});

    // ... implement ALL test cases
}});
```

4. frontend/config/test_config.ts
```typescript
// Test configuration

export interface TestConfig {{
    baseUrl: string;
    browser: string;
    timeout: number;
    headless: boolean;
    screenshotOnFailure: boolean;
}}

export const config: TestConfig = {{
    baseUrl: process.env.BASE_URL || 'http://localhost:3000',
    browser: process.env.BROWSER || 'chrome',
    timeout: 10000,
    headless: process.env.HEADLESS === 'true',
    screenshotOnFailure: true
}};
```

5. frontend/utilities/wait_helpers.ts
```typescript
// Wait and synchronization utilities

import {{ WebDriver, By, until, WebElement }} from 'selenium-webdriver';

export class WaitHelpers {{
    static async waitForPageLoad(driver: WebDriver, timeout: number = 30000): Promise<void> {{
        await driver.wait(
            async () => {{
                const readyState = await driver.executeScript('return document.readyState');
                return readyState === 'complete';
            }},
            timeout
        );
    }}

    static async waitForAjax(driver: WebDriver, timeout: number = 10000): Promise<void> {{
        await driver.wait(
            async () => {{
                const jQueryActive = await driver.executeScript(
                    'return typeof jQuery !== "undefined" ? jQuery.active === 0 : true'
                );
                return jQueryActive;
            }},
            timeout
        );
    }}

    static async waitForElementToDisappear(
        driver: WebDriver,
        locator: By,
        timeout: number = 10000
    ): Promise<void> {{
        await driver.wait(
            until.stalenessOf(await driver.findElement(locator)),
            timeout
        );
    }}
}}
```

6. frontend/utilities/screenshot_helper.ts
```typescript
// Screenshot capture utility

import {{ WebDriver }} from 'selenium-webdriver';
import * as fs from 'fs';
import * as path from 'path';

export class ScreenshotHelper {{
    private static screenshotDir = 'screenshots';

    static async captureScreenshot(
        driver: WebDriver,
        testName: string
    ): Promise<string> {{
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `${{testName}}_${{timestamp}}.png`;
        const filepath = path.join(this.screenshotDir, filename);

        // Ensure directory exists
        if (!fs.existsSync(this.screenshotDir)) {{
            fs.mkdirSync(this.screenshotDir, {{ recursive: true }});
        }}

        const screenshot = await driver.takeScreenshot();
        fs.writeFileSync(filepath, screenshot, 'base64');
        
        return filepath;
    }}
}}
```

7. frontend/fixtures/test_data.ts
```typescript
// Test data fixtures

export const testUsers = {{
    validUser: {{
        username: 'testuser',
        password: 'Test@123',
        email: 'test@example.com'
    }},
    invalidUser: {{
        username: 'invalid',
        password: 'wrong'
    }},
    adminUser: {{
        username: 'admin',
        password: 'Admin@123',
        email: 'admin@example.com'
    }}
}};

export const testData = {{
    urls: {{
        login: '/login',
        dashboard: '/dashboard',
        profile: '/profile'
    }},
    messages: {{
        loginSuccess: 'Login successful',
        loginError: 'Invalid credentials'
    }}
}};
```

8. jest.config.js
```javascript
module.exports = {{
    preset: 'ts-jest',
    testEnvironment: 'node',
    roots: ['<rootDir>/frontend/tests'],
    testMatch: ['**/*.test.ts'],
    collectCoverage: true,
    coverageDirectory: 'coverage',
    setupFilesAfterEnv: ['<rootDir>/frontend/setup.ts'],
    testTimeout: 30000
}};
```

9. frontend/setup.ts
```typescript
// Jest setup file

import {{ WebDriver }} from 'selenium-webdriver';

// Global setup
beforeAll(() => {{
    console.log('Starting test suite');
}});

afterAll(() => {{
    console.log('Test suite completed');
}});

// Screenshot on failure
afterEach(async function() {{
    if (this.currentTest && this.currentTest.state === 'failed') {{
        // Capture screenshot logic
    }}
}});
```

Generate COMPLETE, PRODUCTION-READY TypeScript code for all files. Each file should:
- Be fully implemented (no TODOs or placeholders)
- Include proper error handling
- Have comprehensive comments
- Be executable immediately
- Follow TypeScript best practices
- Include proper typing
- Implement Page Object Model pattern

Make the code robust enough to handle:
- Element not found scenarios
- Stale element references
- Timing issues
- Browser crashes
- Network delays
"""
        
        response = self.generate_response(prompt, context=context)
        
        automation_code = {
            'gui_automation_code': response,
            'language': 'TypeScript',
            'framework': 'Selenium WebDriver + Jest',
            'test_cases_automated': len(test_cases) if isinstance(test_cases, list) else 'all',
            'created_by': self.name,
            'files_generated': [
                'frontend/pages/base_page.ts',
                'frontend/pages/*.ts',
                'frontend/tests/*.test.ts',
                'frontend/config/test_config.ts',
                'frontend/utilities/wait_helpers.ts',
                'frontend/utilities/screenshot_helper.ts',
                'frontend/fixtures/test_data.ts',
                'jest.config.js',
                'frontend/setup.ts'
            ]
        }
        
        self.log_activity("GUI automation code generated", {
            'test_cases': automation_code['test_cases_automated']
        })
        
        return automation_code
