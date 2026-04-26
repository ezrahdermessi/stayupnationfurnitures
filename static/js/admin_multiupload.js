// Admin Multi-Image Upload Enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Find all file inputs in inline groups
    const fileInputs = document.querySelectorAll('.inline-group input[type="file"]');
    
    fileInputs.forEach(function(input) {
        // Make the file input larger and more visible
        input.style.width = '100%';
        input.style.padding = '15px';
        input.style.border = '2px dashed #e6e1d7';
        input.style.borderRadius = '8px';
        input.style.background = '#faf9f7';
        
        // Style the file selector button
        const style = document.createElement('style');
        style.textContent = `
            input[type="file"]::file-selector-button {
                background: #2c3e50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 500;
                margin-right: 15px;
            }
            input[type="file"]::file-selector-button:hover {
                background: #223140;
            }
        `;
        document.head.appendChild(style);
        
        // Add help text below
        const helpText = document.createElement('small');
        helpText.className = 'form-text text-muted';
        helpText.textContent = 'Hold Ctrl (or Cmd on Mac) to select multiple images at once';
        helpText.style.display = 'block';
        helpText.style.marginTop = '8px';
        
        const parent = input.parentElement;
        if (parent && !parent.querySelector('.form-text')) {
            parent.appendChild(helpText);
        }
    });
});
