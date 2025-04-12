document.addEventListener('DOMContentLoaded', function() {
    // Edit mode toggle
    const toggleEditModeBtn = document.getElementById('toggleEditMode');
    let isEditMode = false;
    
    toggleEditModeBtn.addEventListener('click', function() {
        isEditMode = !isEditMode;
        toggleEditModeBtn.textContent = isEditMode ? 'Завершити редагування' : 'Редагувати';
        toggleEditModeBtn.classList.toggle('btn-primary');
        toggleEditModeBtn.classList.toggle('btn-info');
        
        // Toggle visibility of edit controls
        document.querySelectorAll('.edit-mode-only').forEach(el => {
            el.style.display = isEditMode ? '' : 'none';
        });
        
        // Toggle edit-mode class on the container
        document.getElementById('chapters-container').classList.toggle('edit-mode');
        
        // Toggle Sortable functionality
        if (isEditMode) {
            initSortable();
        } else {
            destroySortable();
        }
    });
    
    // Sortable instances
    let chaptersSortable = null;
    let itemsSortables = [];
    
    function initSortable() {
        // init Sortable for chapters
        const chaptersContainer = document.getElementById('chapters-container');
        if (chaptersContainer) {
            chaptersSortable = new Sortable(chaptersContainer, {
                handle: '.drag-handle',
                animation: 150,
                onEnd: function(evt) {
                    const chapters = Array.from(chaptersContainer.children).map((el, index) => {
                        return {
                            id: el.dataset.id,
                            position: index
                        };
                    });
                    
                    // send updated positions to server
                    fetch('{{ url_for("canon.update_chapters_order", canon_id=canon.id) }}', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ chapters: chapters }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Позиції глав оновлено');
                        } else {
                            console.error('Помилка оновлення позицій глав');
                        }
                    });
                }
            });
        }
        
        // init Sortable for items in each chapter
        const itemsContainers = document.querySelectorAll('.items-container');
        itemsContainers.forEach(container => {
            const sortable = new Sortable(container, {
                handle: '.drag-handle',
                animation: 150,
                onEnd: function(evt) {
                    const chapterId = container.dataset.chapterId;
                    const items = Array.from(container.children).map((el, index) => {
                        return {
                            id: el.dataset.id,
                            position: index
                        };
                    });
                    
                    // send updated positions to server
                    fetch(`{{ url_for("canon.update_items_order", chapter_id=0) }}`.replace('0', chapterId), {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ items: items }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Позиції елементів оновлено');
                        } else {
                            console.error('Помилка оновлення позицій елементів');
                        }
                    });
                }
            });
            itemsSortables.push(sortable);
        });
    }
    
    function destroySortable() {
        if (chaptersSortable) {
            chaptersSortable.destroy();
            chaptersSortable = null;
        }
        
        itemsSortables.forEach(sortable => {
            sortable.destroy();
        });
        itemsSortables = [];
    }
}); 