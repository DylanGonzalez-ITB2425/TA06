function calcularConsum() {
    // Obtenir valors dels inputs
    const minAigua = parseFloat(document.getElementById("min_aigua").value);
    const maxAigua = parseFloat(document.getElementById("max_aigua").value);
    const dies = parseInt(document.getElementById("dies").value);

    // Càlcul del consum total estimat per l'any
    const mitjana = (minAigua + maxAigua) / 2;
    const consumTotal = mitjana * dies;

    // Mostrar resultats
    document.getElementById("total_consum").textContent = `Consum total estimat d'aigua per l'any: ${consumTotal.toFixed(2)}L`;
    document.getElementById("diferencia").textContent = `Diferència estimada entre mínim i màxim: ${(maxAigua - minAigua).toFixed(2)}L`;
}
