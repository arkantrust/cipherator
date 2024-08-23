const file = document.getElementById('file');
const filename = document.getElementById('filename');

// set the filename to the name of the file
file.addEventListener('change', (e) => {
  filename.textContent = e.target.files[0].name;
});