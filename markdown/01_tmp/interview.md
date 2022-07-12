# Interview - Associate Director (AT&T)

ADA Compliance - American Disabilities Act
- Size of Text
- Color Pallet
- Audio Support for Text Readout

## RWD

- Mobile First (start on a mobile device then build out)
- Fluid Layouts (used percentages to always scale appropriately)
- Media Queries (custom CSS to adapt to the device size)

### 12 Column System
- Desktop (12 columns)
- Tablet (8 columns)
- Mobile (4 columns)

As the screen is resized to view port based upon Media Query. The media query applies
special formatting corresponding to the size of the browser screen.

### Base-line Grid System
Allows you to more consistently align objects. Can be used in conjunction with the 
12 Grid System.

#### Gutter width

Increase/decrease width between elements, i.e., columns

## Pixels (px) vs EM vs REM

### Citigroup
Content Managemnt System (CMS)
- Page Templates used to create specific pages.
- The specific pages used predefined object names to attach content. 
- The content was cached via platform component

mFoundary to do adaptive screens - Failure... did not go to production. This was a man-in-the-middle
approach that would intercept the response from the full-sized screen and adapt to a supported
user-agent. 

This approach was identified early as a brittle approach that would easily break when the
front-end layout changed even with the smallest change in screen elements.

RWD using Bootstrap
Native development using Kony (similar to Titanium) writing Lua script then JavaScript
that is then transformed into native languages per user selected output, i.e., HTML4, HTML5,
Android (version), iOS/iPhone (version), Tablet, Blackberry, Windows Phone, etc.


### Black Knight
Sprint Management
CA Rally -- Similar to Jira


### Heavy Water

Used a third-party designer to create our 

#### Angular Material -> Material Grid List vs Media Queries

Best of both worlds pull Bootstrap into Angular Material

Angular Material has great Components... but no support for CSS Reset, CSS Layout, CSS Utilities
Bootstrap has great CSS Reset, CSS Layout, CSS Utilities... but no Components 

SO USE THEM BOTH!
