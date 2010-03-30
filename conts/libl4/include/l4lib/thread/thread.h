#ifndef __L4_THREAD_H__
#define __L4_THREAD_H__

#include <l4lib/arch/utcb.h>
#include <l4lib/arch/types.h>

struct l4_thread_struct {
	l4id_t tlid;			/* Thread local id */
	struct task_ids ids;		/* Thread L4-defined ids */
	struct utcb *utcb;		/* Thread utcb */
	unsigned long stack_start;	/* Thread start of stack */
};


/* -- Bora start -- */

/*
  * A helper macro easing utcb space creation,
  * FIXME: We need to fix address allocation path, so as to use
  * actual size of units instead of page size
  */
#define DECLARE_UTCB_SPACE(name, entries) \
	char name[entries * PAGE_SIZE] ALIGN(PAGE_SIZE);

int l4_set_stack_params(unsigned long stack_top,
			unsigned long stack_bottom,
			unsigned long stack_size);
int l4_set_utcb_params(unsigned long utcb_start, unsigned long utcb_end);

int l4_thread_create(struct task_ids *ids, unsigned int flags,
			int (*func)(void *), void *arg);
void l4_thread_exit(int retval);

/* -- Bora start -- */

#endif /* __L4_THREAD_H__ */