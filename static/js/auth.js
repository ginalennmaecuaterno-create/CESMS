/**
 * CESMS Authentication JavaScript
 * Handles form validation, password toggle, flash messages, and user interactions
 */

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeAuth();
});

/**
 * Initialize authentication functionality
 */
function initializeAuth() {
    // Initialize all components
    initializeFlashMessages();
    initializePasswordToggle();
    initializeFormValidation();
    initializePasswordStrength();
    initializeFormSubmission();
    initializeAccessibility();
    
    // Auto-focus first input
    const firstInput = document.querySelector('.form-input');
    if (firstInput) {
        firstInput.focus();
    }
}

/**
 * Check if current page is signup
 */
function isSignupPage() {
    return document.querySelector('input[name="full_name"]') !== null;
}

/**
 * Initialize flash message functionality
 */
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            dismissFlashMessage(message);
        }, 5000);
        
        // Manual dismiss on close button click
        const closeBtn = message.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissFlashMessage(message);
            });
        }
    });
}

/**
 * Dismiss flash message with animation
 */
function dismissFlashMessage(message) {
    message.style.animation = 'slideOutUp 0.3s ease forwards';
    setTimeout(() => {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
        }
    }, 300);
}

/**
 * Initialize password visibility toggle
 */
function initializePasswordToggle() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        const toggleBtn = createPasswordToggle();
        input.parentNode.style.position = 'relative';
        input.parentNode.appendChild(toggleBtn);
        
        toggleBtn.addEventListener('click', () => {
            togglePasswordVisibility(input, toggleBtn);
        });
    });
}

/**
 * Create password toggle button
 */
function createPasswordToggle() {
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'password-toggle';
    toggleBtn.innerHTML = '👁️';
    toggleBtn.setAttribute('aria-label', 'Toggle password visibility');
    toggleBtn.style.position = 'absolute';
    toggleBtn.style.right = '12px';
    toggleBtn.style.top = '12px';
    toggleBtn.style.zIndex = '10';
    return toggleBtn;
}

/**
 * Toggle password visibility
 */
function togglePasswordVisibility(input, toggleBtn) {
    if (input.type === 'password') {
        input.type = 'text';
        toggleBtn.innerHTML = '🙈';
        toggleBtn.setAttribute('aria-label', 'Hide password');
    } else {
        input.type = 'password';
        toggleBtn.innerHTML = '👁️';
        toggleBtn.setAttribute('aria-label', 'Show password');
    }
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('.form-input');
        
        inputs.forEach(input => {
            // Real-time validation with debounce
            let timeout;
            input.addEventListener('input', () => {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    validateField(input);
                }, 300);
            });
            
            // Validation on blur
            input.addEventListener('blur', () => {
                validateField(input);
            });
        });
    });
}

/**
 * Validate individual field
 */
function validateField(input) {
    const value = input.value.trim();
    const fieldName = input.name;
    let isValid = true;
    let errorMessage = '';
    
    // Remove existing error styling
    input.classList.remove('error', 'success');
    removeErrorMessage(input);
    
    // Required field validation
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = `${getFieldLabel(input)} is required.`;
    }
    
    // Email validation
    if (fieldName === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address.';
    }
    
    // Student ID validation (only on signup page)
    if (fieldName === 'student_id' && value && !isValidStudentId(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid student ID.';
    }
    
    // Password validation - ONLY enforce strength requirements on signup page
    if (fieldName === 'password' && value && isSignupPage()) {
        const passwordStrength = calculatePasswordStrength(value);
        updatePasswordStrength(passwordStrength);
        
        if (passwordStrength.score < 2) {
            isValid = false;
            errorMessage = 'Password is too weak. Please use a stronger password.';
        }
    } else if (fieldName === 'password' && value && !isSignupPage()) {
        // On login page, just check if password is not empty (already handled above)
        // Don't show strength feedback
    }
    
    // Confirm password validation (only on signup page)
    if (fieldName === 'confirm_password' && value) {
        const passwordInput = document.querySelector('input[name="password"]');
        if (passwordInput && value !== passwordInput.value) {
            isValid = false;
            errorMessage = 'Passwords do not match.';
        }
    }
    
    // Apply validation styling
    if (isValid && value) {
        input.classList.add('success');
    } else if (!isValid) {
        input.classList.add('error');
        showErrorMessage(input, errorMessage);
    }
    
    return isValid;
}

/**
 * Get field label for error messages
 */
function getFieldLabel(input) {
    const label = document.querySelector(`label[for="${input.id}"]`);
    return label ? label.textContent.replace(' *', '') : input.placeholder || 'This field';
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate student ID format
 */
function isValidStudentId(studentId) {
    const studentIdRegex = /^02\d{2}-\d{4}$/;
    return studentIdRegex.test(studentId);
}

/**
 * Show error message
 */
function showErrorMessage(input, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.id = `${input.name}-error`;
    input.parentNode.appendChild(errorDiv);
}

/**
 * Remove error message
 */
function removeErrorMessage(input) {
    const existingError = document.getElementById(`${input.name}-error`);
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Initialize password strength meter (only on signup page)
 */
function initializePasswordStrength() {
    // Only run on signup page
    if (!isSignupPage()) return;
    
    const passwordInput = document.querySelector('input[name="password"]');
    if (!passwordInput) return;
    
    const strengthMeter = document.querySelector('.strength-meter');
    const strengthFill = document.querySelector('.strength-fill');
    const strengthText = document.querySelector('.strength-text');
    const requirements = document.querySelectorAll('.requirement');
    
    if (!strengthMeter || !strengthFill || !strengthText) return;
    
    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        const strength = calculatePasswordStrength(password);
        updatePasswordStrength(strength);
        updatePasswordRequirements(password, requirements);
    });
}

/**
 * Calculate password strength
 */
function calculatePasswordStrength(password) {
    let score = 0;
    let feedback = '';
    
    // Length check
    if (password.length >= 8) score++;
    else feedback += 'At least 8 characters. ';
    
    // Uppercase check
    if (/[A-Z]/.test(password)) score++;
    else feedback += 'One uppercase letter. ';
    
    // Lowercase check
    if (/[a-z]/.test(password)) score++;
    else feedback += 'One lowercase letter. ';
    
    // Number check
    if (/\d/.test(password)) score++;
    else feedback += 'One number. ';
    
    // Special character check
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;
    
    // Determine strength level
    let level = 'weak';
    if (score >= 4) level = 'strong';
    else if (score >= 2) level = 'medium';
    
    return {
        score: score,
        level: level,
        feedback: feedback
    };
}

/**
 * Update password strength display
 */
function updatePasswordStrength(strength) {
    const strengthFill = document.querySelector('.strength-fill');
    const strengthText = document.querySelector('.strength-text');
    
    if (strengthFill) {
        strengthFill.className = `strength-fill ${strength.level}`;
    }
    
    if (strengthText) {
        const levelText = strength.level.charAt(0).toUpperCase() + strength.level.slice(1);
        strengthText.textContent = `Password strength: ${levelText}`;
    }
}

/**
 * Update password requirements checklist
 */
function updatePasswordRequirements(password, requirements) {
    const checks = [
        password.length >= 8,
        /[A-Z]/.test(password),
        /[a-z]/.test(password),
        /\d/.test(password)
    ];
    
    requirements.forEach((requirement, index) => {
        if (checks[index]) {
            requirement.classList.add('valid');
        } else {
            requirement.classList.remove('valid');
        }
    });
}

/**
 * Initialize form submission handling
 */
function initializeFormSubmission() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form)) {
                e.preventDefault();
                return false;
            }
            
            // Show loading state
            showLoadingState(form);
        });
    });
}

/**
 * Validate entire form
 */
function validateForm(form) {
    const inputs = form.querySelectorAll('.form-input[required]');
    let isFormValid = true;
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isFormValid = false;
        }
    });
    
    // Special validation for signup form
    if (form.querySelector('input[name="confirm_password"]')) {
        const password = form.querySelector('input[name="password"]').value;
        const confirmPassword = form.querySelector('input[name="confirm_password"]').value;
        
        if (password !== confirmPassword) {
            showErrorMessage(form.querySelector('input[name="confirm_password"]'), 'Passwords do not match.');
            isFormValid = false;
        }
    }
    
    return isFormValid;
}

/**
 * Show loading state on form submission
 */
function showLoadingState(form) {
    const submitBtn = form.querySelector('.form-button');
    const originalText = submitBtn.textContent;
    
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    submitBtn.setAttribute('data-original-text', originalText);
    submitBtn.textContent = 'Processing...';
}

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    // Add ARIA labels to form inputs
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
        if (!input.getAttribute('aria-label')) {
            const label = document.querySelector(`label[for="${input.id}"]`);
            if (label) {
                input.setAttribute('aria-label', label.textContent);
            }
        }
    });
    
    // Add ARIA live region for dynamic messages
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    document.body.appendChild(liveRegion);
    
    // Announce form errors to screen readers
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList') {
                const errorMessages = document.querySelectorAll('.error-message');
                errorMessages.forEach(error => {
                    if (error.textContent && !error.getAttribute('data-announced')) {
                        liveRegion.textContent = error.textContent;
                        error.setAttribute('data-announced', 'true');
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

/**
 * Utility function to show flash message
 */
function showFlashMessage(message, type = 'info') {
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    const flashDiv = document.createElement('div');
    flashDiv.className = `flash-message ${type}`;
    flashDiv.innerHTML = `
        <span>${message}</span>
        <button class="close-btn" aria-label="Close message">&times;</button>
    `;
    
    flashContainer.appendChild(flashDiv);
    
    // Auto-dismiss
    setTimeout(() => {
        dismissFlashMessage(flashDiv);
    }, 5000);
    
    // Manual dismiss
    flashDiv.querySelector('.close-btn').addEventListener('click', () => {
        dismissFlashMessage(flashDiv);
    });
}

/**
 * Create flash message container if it doesn't exist
 */
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    const formContainer = document.querySelector('.auth-form-container');
    if (formContainer) {
        formContainer.insertBefore(container, formContainer.firstChild);
    }
    return container;
}

/**
 * Utility function to clear all form errors
 */
function clearFormErrors(form) {
    const errorMessages = form.querySelectorAll('.error-message');
    errorMessages.forEach(error => error.remove());
    
    const inputs = form.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.classList.remove('error', 'success');
    });
}

/**
 * Utility function to reset form
 */
function resetForm(form) {
    form.reset();
    clearFormErrors(form);
    
    // Reset password strength
    const strengthFill = document.querySelector('.strength-fill');
    if (strengthFill) {
        strengthFill.className = 'strength-fill';
    }
    
    const strengthText = document.querySelector('.strength-text');
    if (strengthText) {
        strengthText.textContent = '';
    }
    
    // Reset requirements
    const requirements = document.querySelectorAll('.requirement');
    requirements.forEach(req => req.classList.remove('valid'));
}

// Add CSS for screen reader only content
const style = document.createElement('style');
style.textContent = `
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    @keyframes slideOutUp {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(-20px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);