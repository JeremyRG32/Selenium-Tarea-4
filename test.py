from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def login(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys("Admin")
    
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

def test_login_exitoso(setup):
    driver = setup
    driver.get("https://opensource-demo.orangehrmlive.com/")
    
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    
    username_field.send_keys("Admin")
    password_field.send_keys("admin123")
    login_button.click()

    dashboard_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")))
    assert dashboard_header.text == "Dashboard"
    driver.save_screenshot("results/login_exitoso.png")

def test_login_incorrecto(setup):
    driver = setup
    driver.get("https://opensource-demo.orangehrmlive.com/")
    
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    
    username_field.send_keys("Admin")
    password_field.send_keys("wrongpassword")
    login_button.click()
    
    error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text")))
    assert "Invalid credentials" in error_message.text
    assert "dashboard" not in driver.current_url.lower()
    driver.save_screenshot("results/login_incorrecto.png")

def test_agregar_empleado(setup):
    driver = setup
    login(driver)
    
    wait = WebDriverWait(driver, 10)

    pim_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "PIM")))
    pim_menu.click()

    add_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add Employee")))
    add_button.click()

    first_name = wait.until(EC.presence_of_element_located((By.NAME, "firstName")))
    last_name = driver.find_element(By.NAME, "lastName")
    
    first_name.send_keys("Jeremy")
    last_name.send_keys("Reyes")

    save_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    save_button.click()

    wait.until(
        EC.url_contains("/pim/viewPersonalDetails/empNumber/")
    )

    profile_name = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".orangehrm-edit-employee-name h6"))
    )
    assert "Jeremy Reyes" in profile_name.text
    time.sleep(2)
    driver.save_screenshot("results/employee/agregar_empleado.png")

def test_buscar_empleado_existente(setup):
    driver = setup
    login(driver)

    wait = WebDriverWait(driver, 10)

    pim_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "PIM")))
    pim_menu.click()

    search_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")))
    search_name_field.send_keys("Jeremy Reyes")

    search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    search_button.click()

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row"))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
    assert any("Jeremy" in row.text and "Reyes" in row.text for row in rows)

    driver.save_screenshot("results/employee/buscar_empleado_existente.png")

def test_editar_empleado(setup):
    driver = setup
    login(driver)
    wait = WebDriverWait(driver, 15)
    
    pim_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "PIM")))
    pim_menu.click()
    
    search_name_field = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(text(),'Employee Name')]/following::input[1]")
        )
    )
    search_name_field.send_keys("Jeremy Reyes")
    
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".oxd-autocomplete-dropdown")
            )
        )
        first_suggestion = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".oxd-autocomplete-option span")
            )
        )
        first_suggestion.click()
    except:
        pass
    
    search_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Search']")
        )
    )
    search_button.click()
    
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
        )
    )
    
    edit_button = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "bi-pencil-fill")
        )
    )
    edit_button.click()
    
    wait.until(
        EC.presence_of_element_located((By.NAME, "middleName"))
    )
  
    middle_name = driver.find_element(By.NAME, "middleName")
    middle_name.clear()
    time.sleep(2)
    driver.save_screenshot("results/employee/empleado_editar_1.png")
    middle_name.send_keys("Juan")
    
    save_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Save']")
        )
    )
    save_button.click()
    
    success_message = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".oxd-toast-container .oxd-toast--success")
        )
    )
    driver.save_screenshot("results/employee/empleado_editar_2.png")
    assert "Successfully Updated" in success_message.text

    pim_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "PIM")))
    pim_menu.click()

    search_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")))
    search_name_field.send_keys("Jeremy Juan Reyes")

    search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    search_button.click()

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row"))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
    assert any("Jeremy Juan" in row.text and "Reyes" in row.text for row in rows)
    
    driver.save_screenshot("results/employee/empleado_editar_3.png")

def test_eliminar_empleado(setup):
    driver = setup
    login(driver)
    wait = WebDriverWait(driver, 15)
    
    pim_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "PIM")))
    pim_menu.click()
    
    search_name_field = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(text(),'Employee Name')]/following::input[1]")
        )
    )
    search_name_field.send_keys("Jeremy Juan Reyes")
    
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-autocomplete-dropdown")))
    first_suggestion = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".oxd-autocomplete-option span"))
    )
    first_suggestion.click()
    
    search_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search']"))
    )
    search_button.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")))
    driver.save_screenshot("results/employee/empleado_eliminar_1.png")
    
    delete_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(),'Jeremy')]/ancestor::div[@role='row']//button[contains(@class,'oxd-icon-button')][.//i[contains(@class,'bi-trash')]]")
        )
    )
    delete_button.click()
    
    confirm_delete = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Yes, Delete']")
        )
    )
    confirm_delete.click()
    
    success_message = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-toast-container .oxd-toast--success"))
    )
    assert "Successfully Deleted" in success_message.text
    driver.save_screenshot("results/employee/empleado_eliminar_2.png")
    
    search_button.click()
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".oxd-table-loader")))
    
 
    try:
        no_records = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='No Records Found']"))
        )
        driver.save_screenshot("results/employee/empleado_eliminar_3.png")
    except:
        rows = driver.find_elements(By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
        assert not any("Jeremy Juan Reyes" in row.text for row in rows), "Employee still exists after deletion"
        driver.save_screenshot("results/employee/empleado_eliminar_3_alternative.png")