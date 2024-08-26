document.getElementById('mensualidades').addEventListener('wheel', function(event) {
    if (event.deltaY > 0) {
        this.scrollLeft += 100;
    } else {
        this.scrollLeft -= 100;
    }
});
