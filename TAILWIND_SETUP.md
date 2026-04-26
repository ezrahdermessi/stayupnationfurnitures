# Tailwind CSS configuration for Django

1. Install Node.js (if not already installed)
2. Run: npm install -D tailwindcss postcss autoprefixer
3. Run: npx tailwindcss init -p
4. Configure tailwind.config.js to scan your Django templates:
   content: [
     './templates/**/*.html',
     './**/templates/**/*.html',
   ]
5. Add Tailwind directives to static/css/style.css:
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
6. Build Tailwind: npx tailwindcss -i ./static/css/style.css -o ./static/css/tailwind.css --watch
7. Load tailwind.css in your base.html:
   <link href="{% static 'css/tailwind.css' %}" rel="stylesheet">

After setup, refactor templates to use Tailwind classes for a modern UI.
