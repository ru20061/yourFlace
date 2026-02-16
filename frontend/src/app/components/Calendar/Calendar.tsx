"use client";

import { useState } from "react";
import "./calendar.css";

export interface CalendarItem {
  type: "fanPost" | "artistPost" | "image" | "video" | "event";
  label: string;
}

interface CalendarProps {
  selectedDate: Date | null;
  onDateSelect: (date: Date) => void;
  /** YYYY-MM-DD → 해당 날짜의 콘텐츠 목록 */
  dateItems?: Record<string, CalendarItem[]>;
  /** 하위 호환: 이벤트 날짜 문자열 배열 (dateItems 우선) */
  eventDates?: string[];
}

const WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"];

const TYPE_CONFIG: Record<CalendarItem["type"], { label: string; cls: string }> = {
  fanPost:    { label: "유저",   cls: "tag-fan-post" },
  artistPost: { label: "아티스트", cls: "tag-artist-post" },
  image:      { label: "이미지", cls: "tag-image" },
  video:      { label: "동영상", cls: "tag-video" },
  event:      { label: "이벤트", cls: "tag-event" },
};

const MAX_TAGS = 2;

export default function Calendar({ selectedDate, onDateSelect, dateItems = {}, eventDates = [] }: CalendarProps) {
  const today = new Date();
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(today.getMonth());

  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const firstDayOfWeek = new Date(currentYear, currentMonth, 1).getDay();
  const daysInPrevMonth = new Date(currentYear, currentMonth, 0).getDate();

  const prevMonth = () => {
    if (currentMonth === 0) {
      setCurrentYear((y) => y - 1);
      setCurrentMonth(11);
    } else {
      setCurrentMonth((m) => m - 1);
    }
  };

  const nextMonth = () => {
    if (currentMonth === 11) {
      setCurrentYear((y) => y + 1);
      setCurrentMonth(0);
    } else {
      setCurrentMonth((m) => m + 1);
    }
  };

  const cells: { day: number; isCurrentMonth: boolean; date: Date }[] = [];

  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const d = daysInPrevMonth - i;
    cells.push({ day: d, isCurrentMonth: false, date: new Date(currentYear, currentMonth - 1, d) });
  }
  for (let d = 1; d <= daysInMonth; d++) {
    cells.push({ day: d, isCurrentMonth: true, date: new Date(currentYear, currentMonth, d) });
  }
  const remaining = 7 - (cells.length % 7);
  if (remaining < 7) {
    for (let d = 1; d <= remaining; d++) {
      cells.push({ day: d, isCurrentMonth: false, date: new Date(currentYear, currentMonth + 1, d) });
    }
  }

  const toKey = (date: Date) => {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    return `${y}-${m}-${d}`;
  };

  const isToday = (date: Date) => date.toDateString() === today.toDateString();
  const isSelected = (date: Date) => selectedDate?.toDateString() === date.toDateString();

  const getItems = (date: Date): CalendarItem[] => {
    const key = toKey(date);
    if (dateItems[key]?.length) return dateItems[key];
    if (eventDates.includes(key)) return [{ type: "event", label: "이벤트" }];
    return [];
  };

  // 같은 type끼리 묶어서 개수 표시
  const summarize = (items: CalendarItem[]) => {
    const countByType = new Map<CalendarItem["type"], number>();
    for (const item of items) {
      countByType.set(item.type, (countByType.get(item.type) || 0) + 1);
    }
    return Array.from(countByType.entries()).map(([type, count]) => ({
      type,
      count,
      ...TYPE_CONFIG[type],
    }));
  };

  return (
    <div className="calendar">
      <div className="calendar-header">
        <span className="calendar-month">{currentYear}년 {currentMonth + 1}월</span>
        <div className="calendar-nav">
          <button type="button" onClick={prevMonth}>&lt;</button>
          <button type="button" onClick={nextMonth}>&gt;</button>
        </div>
      </div>
      <div className="calendar-weekdays">
        {WEEKDAYS.map((day) => (
          <div key={day} className="calendar-weekday">{day}</div>
        ))}
      </div>
      <div className="calendar-days">
        {cells.map((cell, idx) => {
          const items = getItems(cell.date);
          const summary = summarize(items);
          const hasContent = summary.length > 0;
          const visibleTags = summary.slice(0, MAX_TAGS);
          const extraCount = summary.length - MAX_TAGS;

          return (
            <div
              key={idx}
              className={[
                "calendar-day",
                !cell.isCurrentMonth && "other-month",
                isToday(cell.date) && "today",
                isSelected(cell.date) && "selected",
                hasContent && "has-content",
              ].filter(Boolean).join(" ")}
              onClick={() => onDateSelect(cell.date)}
            >
              <span className="calendar-day-num">{cell.day}</span>
              {hasContent && (
                <div className="calendar-day-tags">
                  {visibleTags.map((tag) => (
                    <span key={tag.type} className={`calendar-tag ${tag.cls}`}>
                      {tag.label}{tag.count > 1 ? ` ${tag.count}` : ""}
                    </span>
                  ))}
                  {extraCount > 0 && (
                    <span className="calendar-tag tag-more">+{extraCount}</span>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
