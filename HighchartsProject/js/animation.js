export function move(c, x, y) {
  const charts = document.querySelectorAll(".chart");

  // Reset styles for all charts
  charts.forEach((chart) => {
    chart.style.opacity = 0.7;
    chart.style.transform = "scale(0.8)";
    chart.style.pointerEvents = "auto";
  });

  // Highlight the target chart
  c.style.opacity = 1;
  c.style.transform = `translateX(${x}px) translateY(${y}px) scale(1.2)`;

  // Reset previous center chart if it's not the current chart
  if (center_chart && center_chart !== c) {
    center_chart.style.transform = "translateX(0px) translateY(0px) scale(0.8)";
  }

  // Update the center chart
  center_chart = c;
}
export function see_more(district_name) {
  const map = document.getElementById("Hanoimap");
  map.style.display = "none";
}

export function remake_sub_chart_of_Pie(range_name) {
  const sub_charts = document.querySelectorAll(".sub_chart");
  let name;
  // Xác định đường dẫn tệp JSON theo range_name
  switch (range_name) {
    case "Dưới 50 triệu/m²":
      name = "under_50";
      break;
    case "50 đến 100 triệu/m²":
      name = "between_50_100";
      break;
    case "100 đến 150 triệu/m²":
      name = "between_100_150";
      break;
    case "150 đến 200 triệu/m²":
      name = "between_150_200";
      break;
    case "Trên 200 triệu/m²":
      name = "over_200";
      break;
    default:
      console.error("Giá trị range_name không hợp lệ:", range_name);
      return;
  }

  sub_charts.forEach((sub_chart) => {
    sub_chart.remove();
  });

  makeCorrelation("segment", name, false, 900, 0, 30, 50, "sub_chart");
}

export function remake_sub_chart_of_Column(range_name) {
  const sub_charts = document.querySelectorAll(".sub_chart");
  let name = normalizeName(range_name);

  sub_charts.forEach((sub_chart) => {
    sub_chart.remove();
  });

  makeHistoryPrice("type", name, false, 900, 0, 30, 50, "sub_chart");
}

export function remove_sub_chart() {
  const sub_charts = document.querySelectorAll(".sub_chart");

  sub_charts.forEach((chart) => {
    chart.style.opacity = 0;
    setTimeout(() => {
      chart.remove();
    }, 2000);
  });
}

