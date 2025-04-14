document.addEventListener('DOMContentLoaded', function() {
    // Edit mode toggle
    const toggleEditModeBtn = document.getElementById('toggleEditMode');
    let isEditMode = false;
    
    toggleEditModeBtn.addEventListener('click', function() {
        isEditMode = !isEditMode;
        toggleEditModeBtn.textContent = isEditMode ? 'Завершити редагування' : 'Редагувати';
        
        // Toggle button appearance
        if (isEditMode) {
            toggleEditModeBtn.classList.remove('bg-primary', 'hover:bg-primary-dark');
            toggleEditModeBtn.classList.add('bg-blue-500', 'hover:bg-blue-600');
        } else {
            toggleEditModeBtn.classList.remove('bg-blue-500', 'hover:bg-blue-600');
            toggleEditModeBtn.classList.add('bg-primary', 'hover:bg-primary-dark');
        }
        
        // Toggle visibility of edit controls
        document.querySelectorAll('.edit-mode-only').forEach(el => {
            el.classList.toggle('hidden');
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
    let itemsSortables = [];
    
    function initSortable() {
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
                    fetch(window.canonData.updateItemsUrl.replace('0', chapterId), {
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
                            // Можливо, додати повідомлення про помилку тут
                        }
                    })
                    .catch(error => {
                        console.error('Помилка при оновленні позицій:', error);
                        // Можливо, додати повідомлення про помилку тут
                    });
                }
            });
            itemsSortables.push(sortable);
        });
    }
    
    function destroySortable() {
        itemsSortables.forEach(sortable => {
            sortable.destroy();
        });
        itemsSortables = [];
    }
}); 