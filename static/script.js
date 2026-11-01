
const resumeInput = document.getElementById("resume");

if (resumeInput) {
    resumeInput.addEventListener("change", function () {
        const file = this.files[0];

        if (!file) return;

        const allowedExtensions = [".pdf", ".docx"];
        const filename = file.name.toLowerCase();
        const validExtension = allowedExtensions.some(
            extension => filename.endsWith(extension)
        );

        if (!validExtension) {
            alert("Please select a PDF or DOCX file.");
            this.value = "";
        }
    });
}
