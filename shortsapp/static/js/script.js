document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    const uploadProgressContainer = document.getElementById("uploadProgressContainer");
    const uploadProgressBar = document.getElementById("uploadProgressBar");
    const uploadStatus = document.getElementById("uploadStatus");

    const generateBtn = document.getElementById("generateBtn");
    const genProgressContainer = document.getElementById("genProgressContainer");
    const genProgressBar = document.getElementById("genProgressBar");

    if (generateBtn) {
        generateBtn.addEventListener("click", function () {
            genProgressContainer.style.display = "block";
            genProgressBar.style.width = "10%";

            let fakeGenProgress = 10;
            const genInterval = setInterval(() => {
                fakeGenProgress += 10;
                if (fakeGenProgress >= 90) fakeGenProgress = 90;
                genProgressBar.style.width = fakeGenProgress + "%";
            }, 700);

            setTimeout(() => {
                clearInterval(genInterval);
                genProgressBar.style.width = "100%";
            }, 8000); // 대략 8초 후 완료 가정 (실제 생성 시간에 맞게 조절)
        });
    }

    if (uploadBtn) {
        uploadBtn.addEventListener("click", function () {
            uploadProgressContainer.style.display = "block";
            uploadProgressBar.style.width = "20%";

            let fakeProgress = 20;
            const interval = setInterval(() => {
                fakeProgress += 10;
                if (fakeProgress >= 90) fakeProgress = 90;
                uploadProgressBar.style.width = fakeProgress + "%";
            }, 500);

            fetch("/upload/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                }
            })
            .then(response => response.json())
            .then(data => {
                clearInterval(interval);
                uploadProgressBar.style.width = "100%";
                if (data.success) {
                    uploadStatus.innerHTML =
                        `<p>✅ 업로드 완료! <a href="https://youtu.be/${data.video_id}" target="_blank">영상 보기</a></p>`;
                } else {
                    uploadStatus.textContent = "❌ 업로드 실패: " + data.error;
                    uploadProgressBar.style.background = "#888";
                }
            });
        });
    }
});
