# PWA Icons Setup

## Required Icons

For the PWA to work properly, you need to create the following icon files in this directory:

1. **icon-192.png** - 192x192 pixels
2. **icon-512.png** - 512x512 pixels

## How to Create Icons

### Option 1: Using Online Tools (Recommended)
1. Go to https://realfavicongenerator.net/ or https://www.pwabuilder.com/imageGenerator
2. Upload your logo/icon (preferably 512x512 or higher)
3. Download the generated icons
4. Place `icon-192.png` and `icon-512.png` in this directory

### Option 2: Manual Creation
1. Create a 512x512 PNG image with:
   - A shield icon with a medical cross
   - Blue and green gradient background
   - "MediScan" text (optional)
2. Resize to 192x192 for the smaller icon
3. Save both files in this directory

## Temporary Placeholder

Until you create proper icons, the PWA will still work but won't have custom icons when installed.

## Icon Design Guidelines

- **Purpose**: Medical/Health verification app
- **Colors**: Blue (#3b82f6) and Green (#10b981) gradients
- **Symbol**: Shield with medical cross or pill/medicine symbol
- **Style**: Modern, clean, professional
- **Background**: Can be transparent or solid color

## Testing

After adding icons:
1. Run `npm run build`
2. Open the app in Chrome/Edge
3. Check DevTools > Application > Manifest to verify icons load correctly
4. Test installation on mobile device