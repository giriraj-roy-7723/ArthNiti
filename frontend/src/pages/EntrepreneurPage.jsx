import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const EntrepreneurPage = ({ eyebrow, title, description, icon: Icon }) => {
  const { user } = useAuth();

  if (user?.role !== 'enterpreneur') {
    return <Navigate to="/" replace />;
  }

  return (
    <section className="min-h-screen p-8 md:p-12 bg-[radial-gradient(circle_at_top_right,_rgba(37,99,235,0.18),_transparent_35%),linear-gradient(135deg,_#030712,_#111827)]">
      <div className="max-w-5xl mx-auto">
        <p className="text-sm uppercase tracking-[0.25em] text-blue-400 font-bold">{eyebrow}</p>
        <div className="mt-4 flex items-start gap-5">
          <div className="w-14 h-14 shrink-0 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-900/40">
            <Icon size={28} />
          </div>
          <div>
            <h1 className="text-4xl font-extrabold text-white">{title}</h1>
            <p className="mt-3 max-w-2xl text-gray-400 text-lg">{description}</p>
          </div>
        </div>
        <div className="mt-12 grid gap-5 md:grid-cols-3">
          {['Ready to connect your data', 'Personalized insights', 'Actionable next steps'].map((item) => (
            <div key={item} className="rounded-2xl border border-gray-800 bg-gray-900/70 p-6 shadow-xl">
              <div className="h-2 w-12 rounded-full bg-blue-500 mb-5" />
              <h2 className="text-lg font-bold text-white">{item}</h2>
              <p className="mt-2 text-sm text-gray-500">This workspace will appear here as the feature is connected.</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default EntrepreneurPage;