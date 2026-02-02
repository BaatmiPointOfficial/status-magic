// 1. JSON फाइल से वीडियो डेटा लोड करना
async function loadVideos() {
    try {
        const response = await fetch('videos.json');
        const videos = await response.json();
        displayVideos(videos); // शुरू में सभी वीडियो दिखाएं
    } catch (error) {
        console.error("वीडियो लोड करने में गड़बड़:", error);
    }
}

// 2. वीडियो को स्क्रीन पर दिखाने का फंक्शन
function displayVideos(videoList) {
    const container = document.getElementById('video-container');
    container.innerHTML = ''; // पुराना कंटेंट साफ़ करें

    videoList.forEach(video => {
        const videoCard = document.createElement('div');
        videoCard.className = 'video-card';

        // वीडियो का HTML ढांचा (ShareChat स्टाइल)
        videoCard.innerHTML = `
            <video loop preload="metadata" onclick="togglePlay(this)">
                <source src="${video.url}" type="video/mp4">
                आपका ब्राउज़र वीडियो सपोर्ट नहीं करता।
            </video>
            <div class="video-overlay">
                <p class="video-title">${video.public_id.split('/').pop()}</p>
                <div class="action-buttons">
                    <button onclick="shareOnWhatsApp('${video.url}')">🟢 WhatsApp</button>
                    <a href="${video.url}" download class="download-btn">⬇️ डैऊनलोड</a>
                </div>
            </div>
        `;
        container.appendChild(videoCard);
    });

    // पहले वीडियो को अपने आप प्ले करने की कोशिश करें
    const firstVideo = container.querySelector('video');
    if (firstVideo) firstVideo.play().catch(() => {});
}

// 3. कैटेगरी के हिसाब से वीडियो फ़िल्टर करना
async function filterVideos(category) {
    const response = await fetch('videos.json');
    const allVideos = await response.json();

    // बटन का रंग बदलना
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');

    if (category === 'all') {
        displayVideos(allVideos);
    } else {
        // फोल्डर के नाम के हिसाब से फ़िल्टर
        const filtered = allVideos.filter(v => v.public_id.includes(category));
        displayVideos(filtered);
    }
}

// 4. वीडियो प्ले/पॉज कंट्रोल
function togglePlay(video) {
    if (video.paused) {
        video.play();
    } else {
        video.pause();
    }
}

// 5. WhatsApp पर शेयर करने का जुगाड़
function shareOnWhatsApp(videoUrl) {
    const text = "यह धांसू स्टेटस देखो: " + videoUrl;
    window.open("https://api.whatsapp.com/send?text=" + encodeURIComponent(text));
}

// फाइल लोड होते ही वीडियो दिखाना शुरू करें
window.onload = loadVideos;
