interface DispositionCardProps {
  disposition: string;
  priority: string;
}

const DISPOSITION_CONFIG: Record<string, {
  title: string;
  description: string;
  colorClass: string;
  bgClass: string;
  borderClass: string;
  icon: string;
}> = {
  CALL_911: {
    title: 'Call 911 Now',
    description: 'This is a medical emergency. Call 911 immediately.',
    colorClass: 'text-red-700',
    bgClass: 'bg-red-50',
    borderClass: 'border-red-300',
    icon: '🚨',
  },
  ER_NOW: {
    title: 'Go to Emergency Room Now',
    description: 'You should go to the nearest emergency room immediately.',
    colorClass: 'text-orange-700',
    bgClass: 'bg-orange-50',
    borderClass: 'border-orange-300',
    icon: '🏥',
  },
  URGENT_CARE_TODAY: {
    title: 'Seek Urgent Care Today',
    description: 'You should visit an urgent care facility or see a doctor today.',
    colorClass: 'text-amber-700',
    bgClass: 'bg-amber-50',
    borderClass: 'border-amber-300',
    icon: '⚕️',
  },
  PRIMARY_CARE_24_72H: {
    title: 'See Your Doctor Within 24-72 Hours',
    description: 'Schedule an appointment with your primary care provider within the next few days.',
    colorClass: 'text-yellow-700',
    bgClass: 'bg-yellow-50',
    borderClass: 'border-yellow-300',
    icon: '📅',
  },
  SELF_CARE: {
    title: 'Self-Care at Home',
    description: 'Your symptoms may be manageable with home care. Monitor your condition.',
    colorClass: 'text-green-700',
    bgClass: 'bg-green-50',
    borderClass: 'border-green-300',
    icon: '🏠',
  },
};

export function DispositionCard({ disposition, priority }: DispositionCardProps) {
  const config = DISPOSITION_CONFIG[disposition] || DISPOSITION_CONFIG.SELF_CARE;

  return (
    <div className={`rounded-xl border-2 ${config.borderClass} ${config.bgClass} p-6`}>
      <div className="flex items-start gap-4">
        <span className="text-4xl">{config.icon}</span>
        <div>
          <div className="flex items-center gap-2 mb-2">
            <h2 className={`text-2xl font-bold ${config.colorClass}`}>
              {config.title}
            </h2>
            {priority === 'critical' && (
              <span className="px-2 py-1 bg-red-600 text-white text-xs font-bold rounded uppercase">
                Critical
              </span>
            )}
          </div>
          <p className={`text-lg ${config.colorClass}`}>
            {config.description}
          </p>
        </div>
      </div>

      {disposition === 'CALL_911' && (
        <div className="mt-6 p-4 bg-red-100 rounded-lg">
          <p className="text-red-800 font-bold text-center text-xl">
            📞 Call 911 Now
          </p>
          <p className="text-red-700 text-center mt-2">
            Do not drive yourself. Stay on the line with the operator.
          </p>
        </div>
      )}
    </div>
  );
}
