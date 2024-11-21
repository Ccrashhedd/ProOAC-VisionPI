// Cambiar esta sección de los nombres con la conexión a la base de datos
const data = {
  1: ["Ana López", "Carlos Pérez", "María García", "Luis Gómez"],
  2: ["Elena Torres", "José Martínez", "Carmen Rivera", "Miguel Ortiz"],
  3: ["Sofía Herrera", "Daniel Castro", "Isabel Flores", "Pedro Vega"],
  4: ["Isabel Martiñón", "René Garcia", "Mario Castañeda", "Gerardo Reyero"]
};

function updateList() {
  const category = document.getElementById("categorySelect").value;
  const listElement = document.getElementById("nameList");
  listElement.innerHTML = ""; // Limpia la lista

  if (category && data[category]) {
    data[category].forEach((name, index) => {
      const li = document.createElement("li");

      // Label para el nombre
      const nameLabel = document.createElement("label");
      nameLabel.setAttribute("for", `person${index}`);
      nameLabel.textContent = name;

      // Label para la cédula
      const cedulaLabel = document.createElement("label");
      cedulaLabel.setAttribute("for", `cedula${index}`);
      cedulaLabel.textContent = ` - Cédula: 00${category}${index + 1}`;

      // Agregar los labels al li
      li.appendChild(nameLabel);
      li.appendChild(cedulaLabel);

      // Agregar el li a la lista
      listElement.appendChild(li);
    });
  }
}