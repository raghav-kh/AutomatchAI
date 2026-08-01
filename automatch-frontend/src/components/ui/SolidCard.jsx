export default function SolidCard({ children, className = "", hover = false, ...props }) {
  const hoverClass = hover ? "card-hover-effect" : "";
  return (
    <div className={`solid-card rounded-xl p-5 ${hoverClass} ${className}`} {...props}>
      {children}
    </div>
  );
}
