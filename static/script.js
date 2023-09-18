function hitungAkarAPI() {
    const inputNumber = parseFloat(document.getElementById("inputNumber").value);
    
    if (isNaN(inputNumber)) {
        alert("Masukkan angka yang valid.");
        return;
    }
    
    if (inputNumber < 0) {
        alert("Angka harus positif atau nol.");
        return;
    }

    // Mengirim permintaan POST ke API
    fetch('/api/hitung-akar-kuadrat-api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'angka': inputNumber })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Menampilkan hasil di halaman
            document.getElementById("result").textContent = data.hasil.toFixed(2);

            // Menampilkan waktu penghitungan di log
            const logElement = document.getElementById("log");
            const logItem = document.createElement("li");
            logItem.textContent = `[API] Akar kuadrat dari ${inputNumber} adalah ${data.hasil.toFixed(2)} (Waktu: ${data.waktu_penghitungan.toFixed(2)} ms)`;
            logElement.appendChild(logItem);
        }
    })
    .catch(error => {
        console.error('Terjadi kesalahan:', error);
        alert('Terjadi kesalahan saat menghitung akar kuadrat.');
    });
}

function hitungAkarSPSQL() {

        const inputNumber = parseFloat(document.getElementById("inputNumber").value);
        
        if (isNaN(inputNumber)) {
            alert("Masukkan angka yang valid.");
            return;
        }
        
        if (inputNumber < 0) {
            alert("Angka harus positif atau nol.");
            return;
        }
    
        // Mengirim permintaan POST ke API
        fetch('/api/hitung-akar-kuadrat-stored-procedure', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'angka': inputNumber })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                // Menampilkan hasil di halaman
                document.getElementById("result").textContent = data.hasil.toFixed(2);
    
                // Menampilkan waktu penghitungan di log
                const logElement = document.getElementById("log");
                const logItem = document.createElement("li");
                logItem.textContent = `[Stored Procedure] Akar kuadrat dari ${inputNumber} adalah ${data.hasil.toFixed(2)} (Waktu: ${data.waktu_penghitungan.toFixed(2)} ms)`;
                logElement.appendChild(logItem);
            }
        })
        .catch(error => {
            console.error('Terjadi kesalahan:', error);
            alert('Terjadi kesalahan saat menghitung akar kuadrat.');
        });
    }
    
