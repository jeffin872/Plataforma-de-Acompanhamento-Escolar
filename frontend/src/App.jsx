import AppRoutes from "./routes/AppRoutes.jsx";

/**
 * App é intencionalmente enxuto: BrowserRouter e AuthProvider já foram
 * montados em main.jsx (para que hooks como useNavigate/useAuth possam
 * ser usados em qualquer nível da árvore de rotas). Aqui só entra o
 * roteamento em si.
 */
export default function App() {
  return <AppRoutes />;
}
