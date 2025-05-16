document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('nav ul');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('show');
        });
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navMenu.contains(event.target);
        const isClickOnToggle = menuToggle.contains(event.target);
        
        if (!isClickInsideNav && !isClickOnToggle && navMenu.classList.contains('show')) {
            navMenu.classList.remove('show');
        }
    });
    
    // Form Validation
    const joinForm = document.getElementById('join-form');
    if (joinForm) {
        joinForm.addEventListener('submit', function(event) {
            let hasError = false;
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const phoneInput = document.getElementById('phone');
            
            // Reset previous error messages
            document.querySelectorAll('.error-message').forEach(el => el.remove());
            
            // Validate name
            if (!nameInput.value.trim()) {
                displayError(nameInput, 'Name is required');
                hasError = true;
            }
            
            // Validate email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailInput.value.trim())) {
                displayError(emailInput, 'Please enter a valid email address');
                hasError = true;
            }
            
            // Validate phone (optional but if filled, should be valid)
            if (phoneInput.value.trim() && !/^[\d\s()+-]{10,15}$/.test(phoneInput.value.trim())) {
                displayError(phoneInput, 'Please enter a valid phone number');
                hasError = true;
            }
            
            if (hasError) {
                event.preventDefault();
            } else {
                // Form is valid, could add success message or proceed with submission
                alert('Thank you for your submission! We will contact you soon.');
            }
        });
    }
    
    function displayError(inputElement, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = 'red';
        errorDiv.style.fontSize = '0.8rem';
        errorDiv.style.marginTop = '5px';
        
        inputElement.parentNode.appendChild(errorDiv);
        inputElement.style.borderColor = 'red';
    }
    
    // Event Gallery Functionality
    const eventThumbs = document.querySelectorAll('.event-gallery-thumbs .thumb');
    
    if (eventThumbs.length > 0) {
        initEventGallery();
    }
    
    function initEventGallery() {
        const eventThumbs = document.querySelectorAll('.event-gallery-thumbs .thumb');
        
        eventThumbs.forEach(thumb => {
            thumb.addEventListener('click', function(e) {
                e.preventDefault();
                
                const eventId = this.getAttribute('data-event');
                
                if (this.classList.contains('more-photos')) {
                    // Show all photos in the lightbox
                    const mainThumbs = document.querySelectorAll(`.thumb[data-event="${eventId}"]:not(.more-photos)`);
                    const hiddenImages = document.querySelectorAll(`#${eventId}-gallery img`);
                    
                    // Collect all image sources
                    const allImages = [];
                    
                    mainThumbs.forEach(mainThumb => {
                        allImages.push({
                            src: mainThumb.getAttribute('data-image'),
                            caption: mainThumb.querySelector('img').getAttribute('alt')
                        });
                    });
                    
                    hiddenImages.forEach(hiddenImg => {
                        allImages.push({
                            src: hiddenImg.getAttribute('src'),
                            caption: hiddenImg.getAttribute('alt')
                        });
                    });
                    
                    // Open lightbox with all images
                    openEventGallery(allImages, 0);
                } else {
                    // Show single image in lightbox
                    const imgSrc = this.getAttribute('data-image');
                    const caption = this.querySelector('img').getAttribute('alt');
                    
                    // Get all images for this event to allow navigation
                    const relatedThumbs = document.querySelectorAll(`.thumb[data-event="${eventId}"]:not(.more-photos)`);
                    const hiddenImages = document.querySelectorAll(`#${eventId}-gallery img`);
                    
                    const allImages = [];
                    let currentIndex = 0;
                    
                    relatedThumbs.forEach((relThumb, index) => {
                        const src = relThumb.getAttribute('data-image');
                        allImages.push({
                            src: src,
                            caption: relThumb.querySelector('img').getAttribute('alt')
                        });
                        
                        if (src === imgSrc) {
                            currentIndex = index;
                        }
                    });
                    
                    hiddenImages.forEach(hiddenImg => {
                        allImages.push({
                            src: hiddenImg.getAttribute('src'),
                            caption: hiddenImg.getAttribute('alt')
                        });
                    });
                    
                    // Open lightbox gallery starting with the clicked image
                    openEventGallery(allImages, currentIndex);
                }
            });
        });
    }
    
    function openEventGallery(images, startIndex) {
        // Create lightbox container
        const lightbox = document.createElement('div');
        lightbox.className = 'event-lightbox';
        
        // Create image container
        const imgContainer = document.createElement('div');
        imgContainer.className = 'event-lightbox-container';
        
        // Create image element
        const img = document.createElement('img');
        img.src = images[startIndex].src;
        
        // Create caption
        const captionDiv = document.createElement('div');
        captionDiv.className = 'event-lightbox-caption';
        captionDiv.textContent = images[startIndex].caption;
        
        // Create counter
        const counterDiv = document.createElement('div');
        counterDiv.className = 'event-lightbox-counter';
        counterDiv.textContent = `${startIndex + 1} / ${images.length}`;
        
        // Create navigation buttons if there are multiple images
        let currentIndex = startIndex;
        
        if (images.length > 1) {
            // Previous button
            const prevBtn = document.createElement('button');
            prevBtn.className = 'event-lightbox-nav event-lightbox-prev';
            prevBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
            
            // Next button
            const nextBtn = document.createElement('button');
            nextBtn.className = 'event-lightbox-nav event-lightbox-next';
            nextBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
            
            // Navigation functionality
            prevBtn.addEventListener('click', function() {
                currentIndex = (currentIndex - 1 + images.length) % images.length;
                updateImage();
            });
            
            nextBtn.addEventListener('click', function() {
                currentIndex = (currentIndex + 1) % images.length;
                updateImage();
            });
            
            imgContainer.appendChild(prevBtn);
            imgContainer.appendChild(nextBtn);
            
            // Create thumbnails for quick navigation
            const thumbsContainer = document.createElement('div');
            thumbsContainer.className = 'event-lightbox-thumbs';
            
            images.forEach((image, index) => {
                const thumb = document.createElement('div');
                thumb.className = 'thumb';
                if (index === startIndex) {
                    thumb.classList.add('active');
                }
                
                const thumbImg = document.createElement('img');
                thumbImg.src = image.src;
                
                thumb.appendChild(thumbImg);
                thumbsContainer.appendChild(thumb);
                
                thumb.addEventListener('click', function() {
                    // Update the current image
                    currentIndex = index;
                    updateImage();
                    
                    // Update thumbnail highlight
                    document.querySelectorAll('.event-lightbox-thumbs .thumb').forEach(t => t.classList.remove('active'));
                    this.classList.add('active');
                });
            });
            
            lightbox.appendChild(thumbsContainer);
        }
        
        // Create close button
        const closeBtn = document.createElement('span');
        closeBtn.className = 'event-lightbox-close';
        closeBtn.innerHTML = '&times;';
        
        // Close lightbox when clicking close button or outside the image
        closeBtn.addEventListener('click', function() {
            document.body.removeChild(lightbox);
        });
        
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                document.body.removeChild(lightbox);
            }
        });
        
        // Keyboard navigation
        const keyHandler = function(e) {
            if (lightbox.parentNode) {
                if (e.key === 'ArrowLeft' && images.length > 1) {
                    currentIndex = (currentIndex - 1 + images.length) % images.length;
                    updateImage();
                } else if (e.key === 'ArrowRight' && images.length > 1) {
                    currentIndex = (currentIndex + 1) % images.length;
                    updateImage();
                } else if (e.key === 'Escape') {
                    document.body.removeChild(lightbox);
                    document.removeEventListener('keydown', keyHandler);
                }
            }
        };
        
        document.addEventListener('keydown', keyHandler);
        
        function updateImage() {
            img.src = images[currentIndex].src;
            captionDiv.textContent = images[currentIndex].caption;
            counterDiv.textContent = `${currentIndex + 1} / ${images.length}`;
            
            // Update thumbnail highlight
            const thumbs = document.querySelectorAll('.event-lightbox-thumbs .thumb');
            if (thumbs.length) {
                thumbs.forEach(t => t.classList.remove('active'));
                thumbs[currentIndex].classList.add('active');
            }
        }
        
        // Append elements to lightbox and body
        imgContainer.appendChild(img);
        lightbox.appendChild(imgContainer);
        lightbox.appendChild(captionDiv);
        lightbox.appendChild(counterDiv);
        lightbox.appendChild(closeBtn);
        document.body.appendChild(lightbox);
    }
    
    // Gallery Lightbox
    const galleryItems = document.querySelectorAll('.gallery-item');
    if (galleryItems.length > 0) {
        galleryItems.forEach(item => {
            item.addEventListener('click', function() {
                const imgSrc = this.querySelector('img').src;
                const caption = this.querySelector('.gallery-caption') ? 
                    this.querySelector('.gallery-caption').textContent : '';
                
                openLightbox(imgSrc, caption);
            });
        });
    }
    
    function openLightbox(src, caption) {
        // Create lightbox container
        const lightbox = document.createElement('div');
        lightbox.className = 'lightbox';
        lightbox.style.position = 'fixed';
        lightbox.style.top = '0';
        lightbox.style.left = '0';
        lightbox.style.width = '100%';
        lightbox.style.height = '100%';
        lightbox.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
        lightbox.style.display = 'flex';
        lightbox.style.alignItems = 'center';
        lightbox.style.justifyContent = 'center';
        lightbox.style.zIndex = '1000';
        lightbox.style.flexDirection = 'column';
        
        // Create image element
        const img = document.createElement('img');
        img.src = src;
        img.style.maxWidth = '80%';
        img.style.maxHeight = '80%';
        img.style.objectFit = 'contain';
        img.style.border = '5px solid white';
        img.style.boxShadow = '0 0 20px rgba(0, 0, 0, 0.5)';
        
        // Create caption
        if (caption) {
            const captionDiv = document.createElement('div');
            captionDiv.textContent = caption;
            captionDiv.style.color = 'white';
            captionDiv.style.marginTop = '15px';
            captionDiv.style.fontSize = '1.2rem';
            lightbox.appendChild(captionDiv);
        }
        
        // Create close button
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.position = 'absolute';
        closeBtn.style.top = '20px';
        closeBtn.style.right = '30px';
        closeBtn.style.color = 'white';
        closeBtn.style.fontSize = '40px';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.fontWeight = 'bold';
        
        // Close lightbox when clicking close button or outside the image
        closeBtn.addEventListener('click', function() {
            document.body.removeChild(lightbox);
        });
        
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                document.body.removeChild(lightbox);
            }
        });
        
        // Append elements to lightbox and body
        lightbox.appendChild(img);
        lightbox.appendChild(closeBtn);
        document.body.appendChild(lightbox);
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                e.preventDefault();
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 100, // Adjust for header
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}); 