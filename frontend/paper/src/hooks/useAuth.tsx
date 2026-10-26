import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import { api, authToken, type AuthUser } from "@/lib/api";

interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string, confirmPassword: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
  });

  // On mount, verify any stored token with the backend
  useEffect(() => {
    const token = authToken.get();
    if (!token) {
      setState({ user: null, isLoading: false, isAuthenticated: false });
      return;
    }
    api
      .getMe()
      .then((data) => {
        // Token valid but we only have email from /me; decode name from token if possible
        const stored = localStorage.getItem("papertrail.user");
        const parsed = stored ? (JSON.parse(stored) as AuthUser) : null;
        const user: AuthUser = parsed ?? { userId: "", name: "", email: data.email };
        setState({ user, isLoading: false, isAuthenticated: true });
      })
      .catch(() => {
        // Token invalid or expired — clear it
        authToken.clear();
        localStorage.removeItem("papertrail.user");
        setState({ user: null, isLoading: false, isAuthenticated: false });
      });
  }, []);

  const login = async (email: string, password: string) => {
    const user = await api.login(email, password);
    localStorage.setItem("papertrail.user", JSON.stringify(user));
    setState({ user, isLoading: false, isAuthenticated: true });
  };

  const register = async (name: string, email: string, password: string, confirmPassword: string) => {
    const user = await api.register(name, email, password, confirmPassword);
    localStorage.setItem("papertrail.user", JSON.stringify(user));
    setState({ user, isLoading: false, isAuthenticated: true });
  };

  const logout = () => {
    api.logout();
    localStorage.removeItem("papertrail.user");
    setState({ user: null, isLoading: false, isAuthenticated: false });
  };

  return (
    <AuthContext.Provider value={{ ...state, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
