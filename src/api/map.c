/*
 * Space-related system calls.
 *
 * Copyright (C) 2007 Bahadir Balban
 */
#include <l4/generic/tcb.h>
#include INC_API(syscall.h)
#include INC_SUBARCH(mm.h)
#include <l4/api/errno.h>
#include <l4/api/space.h>

int sys_map(unsigned long phys, unsigned long virt, unsigned long npages,
	    unsigned long flags, unsigned int tid)
{
	struct ktcb *target;

	if (tid == current->tid) { /* The easiest case */
		target = current;
		goto found;
	} else 	/* else search the tcb from its hash list */
		if ((target = tcb_find(tid)))
			goto found;

	BUG();
	return -EINVAL;

found:
//	printk("%s (%d) Mapping from 0x%lx to 0x%lxp, %lu pages\n", __FUNCTION__, tid, phys, virt, npages);
	add_mapping_pgd(phys, virt, npages << PAGE_BITS, flags, TASK_PGD(target));

	return 0;
}

/*
 * Unmaps given range from given task. If the complete range is unmapped
 * sucessfully, returns 0. If part of the range was found to be already
 * unmapped, returns -1. This is may or may not be an error.
 */
int sys_unmap(unsigned long virtual, unsigned long npages, unsigned int tid)
{
	struct ktcb *target;
	int ret = 0, retval = 0;

	if (tid == current->tid)
		target = current;
	else if (!(target = tcb_find(tid)))
		return -ESRCH;

	for (int i = 0; i < npages; i++) {
		ret = remove_mapping_pgd(virtual + i * PAGE_SIZE, TASK_PGD(target));
		if (ret)
			retval = ret;
	}

	return retval;
}
