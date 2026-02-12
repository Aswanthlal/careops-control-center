fetch("/api/dashboard/")
  .then(res => res.json())
  .then(data => {
    document.getElementById("todayBookings").innerText = data.today_bookings;
    document.getElementById("unansweredCount").innerText = data.unanswered_conversations;
    document.getElementById("lowStockCount").innerText = data.low_stock_alerts;
    
  });
