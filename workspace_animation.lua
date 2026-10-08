-- Órbita: deriva horizontal con aceleración suave y frenado gradual.
-- 4.5 decisegundos = 450 ms; recorrido del 28% del ancho de la pantalla.
hl.curve("orbitaDrift", {
  type = "bezier",
  points = { { 0.45, 0.0 }, { 0.20, 1.0 } },
})

for _, leaf in ipairs({ "workspaces", "workspacesIn", "workspacesOut" }) do
  hl.animation({
    leaf = leaf,
    enabled = true,
    speed = 4.5,
    bezier = "orbitaDrift",
    style = "slidefade 28%",
  })
end
