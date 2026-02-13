function loadBookings() {
    fetchfetch(window.location.origin + "/api/bookings/")

        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("bookingsTable");
            table.innerHTML = "";

            data.forEach(b => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${b.customer}</td>
                    <td>${b.service}</td>
                    <td>${b.time}</td>
                    <td>${b.status}</td>
                    <td>
                        <button onclick="updateStatus(${b.id}, 'completed')">Completed</button>
                        <button onclick="updateStatus(${b.id}, 'no_show')">No Show</button>
                    </td>
                `;

                table.appendChild(row);
            });
        });
}

function updateStatus(id, status) {
    fetchfetch(window.location.origin + "/api/update-booking/", {

        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            booking_id: id,
            status: status
        })
    }).then(() => loadBookings());
}

loadBookings();
